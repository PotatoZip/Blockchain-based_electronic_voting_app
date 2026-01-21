"""Views related to elections listing, authentication via signed challenges"""

from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from eth_account import Account
from eth_account.messages import encode_defunct
from datetime import datetime, time, timedelta
from django.conf import settings
from django.utils import timezone
from django.db.models import QuerySet
import uuid, secrets

from .models import Election, Voter, VotingSession, AuthChallenge
from .serializers import ElectionListSerializer, ElectionDetailSerializer
from .client import voter_key, has_voted_onchain, mark_voted_and_count, contract


def parse_date(d: str | None):
    if not d:
        return None
    try:
        dt = datetime.strptime(d, "%Y-%m-%d")
        return timezone.make_aware(dt)
    except ValueError:
        return None


class ElectionListView(ListAPIView):
    """View for listing elections with optional filtering by status and date range"""

    serializer_class = ElectionListSerializer

    def get_queryset(self) -> QuerySet[Election]:
        qs = Election.objects.all().order_by("-start_date")
        now = timezone.now()
        status_param = (self.request.query_params.get("status") or "all").lower()
        if status_param == "active":
            qs = qs.filter(start_date__lte=now, end_date__gte=now)
        elif status_param == "archive":
            qs = qs.filter(end_date__lt=now)
        elif status_param == "upcoming":
            qs = qs.filter(start_date__gt=now)

        date_from = parse_date(self.request.query_params.get("date_from"))
        date_to = parse_date(self.request.query_params.get("date_to"))
        if date_from:
            qs = qs.filter(start_date__gte=date_from)
        if date_to:
            end_of_day = timezone.make_aware(
                datetime.combine(date_to.date(), time(23, 59, 59))
            )
            qs = qs.filter(start_date__lte=end_of_day)
        return qs


class ElectionDetailView(RetrieveAPIView):
    """View for retrieving detailed information about a specific election"""

    queryset = Election.objects.all()
    serializer_class = ElectionDetailSerializer


class ChallengeView(APIView):
    """View for generating a nonce challenge for a given address to sign"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        address = (request.data.get("address") or "").strip()
        if not address:
            return Response({"detail": "address required"}, status=400)

        AuthChallenge.purge_expired()
        nonce = "evote:" + secrets.token_hex(16)
        ch, _ = AuthChallenge.objects.update_or_create(
            address=address.lower(),
            defaults={
                "nonce": nonce,
                "expires_at": timezone.now() + timedelta(minutes=10),
            },
        )
        return Response({"nonce": ch.nonce}, status=200)


class VerifyView(APIView):
    """Verify voter's identity by checking signed challenge and voter credentials"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        pesel = (request.data.get("pesel") or "").strip()
        code = (request.data.get("code") or "").strip()
        election_id = request.data.get("election_id")
        address = (request.data.get("address") or "").strip()
        signature = (request.data.get("signature") or "").strip()

        if not pesel or not code or not election_id or not address or not signature:
            return Response({"detail": "Missing fields"}, status=400)

        try:
            ch = AuthChallenge.objects.get(address=address.lower())
        except AuthChallenge.DoesNotExist:
            return Response({"detail": "Challenge not found"}, status=403)
        if ch.expires_at < timezone.now():
            return Response({"detail": "Challenge expired"}, status=403)

        signer = Account.recover_message(
            encode_defunct(text=ch.nonce), signature=signature
        )
        if signer.lower() != address.lower():
            return Response({"detail": "Bad signature"}, status=403)

        try:
            voter = Voter.objects.get(
                pesel=pesel, election_id=election_id, verification_code=code
            )
        except Voter.DoesNotExist:
            return Response({"detail": "Invalid verification code"}, status=403)

        sess = VotingSession.objects.create(
            session_id=uuid.uuid4().hex,
            pesel=pesel,
            email=voter.email,
            election_id=election_id,
            public_address=address,
            is_verified=True,
            next_nonce=1,
        )

        try:
            voter.is_authenticated = True
            voter.save(update_fields=["is_authenticated"])
        except Exception:
            pass

        ch.delete()

        return Response(
            {
                "session_token": sess.session_id,
                "public_address": address,
                "next_nonce": sess.next_nonce,
                "expires_in_seconds": 7200,
            },
            status=200,
        )


class CastVoteView(APIView):
    """Cast a vote for a given choice in an election, verifying voter's session and signature"""

    permission_classes = [permissions.AllowAny]

    def post(self, request, election_id: int):
        session_token = request.data.get("session_token")
        choice_id = request.data.get("choice_id")
        signature = request.data.get("signature")

        if not session_token or choice_id is None or not signature:
            return Response({"detail": "Missing fields"}, status=400)

        try:
            sess = VotingSession.objects.get(
                session_id=session_token, election_id=election_id, is_verified=True
            )
        except VotingSession.DoesNotExist:
            return Response({"detail": "Invalid session"}, status=403)

        if sess.is_expired():
            return Response({"detail": "Session expired"}, status=401)

        try:
            election = Election.objects.get(pk=election_id)
        except Election.DoesNotExist:
            return Response({"detail": "Election not found"}, status=404)

        now = timezone.now()
        if not (election.start_date <= now <= election.end_date):
            return Response({"detail": "Election not active"}, status=400)

        try:
            voter = Voter.objects.get(pesel=sess.pesel, election_id=election_id)
        except Voter.DoesNotExist:
            return Response({"detail": "Voter not found"}, status=404)

        if getattr(voter, "has_voted", False):
            return Response({"detail": "Already voted (local)"}, status=409)

        message = f"vote:{election_id}:{choice_id}:{sess.next_nonce}"
        signer = Account.recover_message(
            encode_defunct(text=message), signature=signature
        )
        if signer.lower() != (sess.public_address or "").lower():
            return Response({"detail": "Bad signature"}, status=403)

        vkey = voter_key(sess.pesel, election_id, settings.SECRET_SALT)
        if has_voted_onchain(vkey):
            return Response({"detail": "Already voted on-chain"}, status=409)

        tx_hash = mark_voted_and_count(election_id, vkey, int(choice_id))

        sess.has_voted = True
        sess.next_nonce = sess.next_nonce + 1
        sess.save(update_fields=["has_voted", "next_nonce"])

        try:
            voter.has_voted = True
            voter.save(update_fields=["has_voted"])
        except Exception:
            pass

        return Response(
            {
                "txHash": tx_hash,
                "public_address": sess.public_address,
                "next_nonce": sess.next_nonce,
            },
            status=200,
        )


class ElectionResultsView(APIView):
    """Returns per-choice counts for a given election by querying the smart contract"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, election_id: int):
        try:
            election = Election.objects.get(pk=election_id)
        except Election.DoesNotExist:
            return Response({"detail": "Election not found"}, status=404)

        now = timezone.now()
        if election.end_date > now:
            return Response({"detail": "Election not finished"}, status=400)

        results = []
        for choice in election.choices.all():
            try:
                count = contract.functions.getChoiceCount(election_id, choice.id).call()
            except Exception as e:
                return Response({"detail": f"Contract call failed: {e}"}, status=500)
            results.append(
                {"choice_id": choice.id, "name": choice.name, "votes": count}
            )

        return Response({"results": results}, status=200)
