from django.shortcuts import render
from django.utils import timezone
from django.db.models import QuerySet
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from datetime import datetime, time, timedelta
from .models import Election, Voter, VerificationSession
from .serializers import ElectionListSerializer
from web3 import Account
from .crypto_keys import encrypt_bytes


def parse_date(d: str | None):
    if not d:
        return None
    try:
        dt = datetime.strptime(d, "%Y-%m-%d")
        return timezone.make_aware(dt)
    except ValueError:
        return None


class ElectionListView(ListAPIView):
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
    queryset = Election.objects.all()
    serializer_class = ElectionListSerializer


class VerifyVoterView(APIView):
    """
    POST /api/elections/<id>/verify/
    body: { pesel: string, code: string }
    response: { session_id: uuid, eth_address: "0x..." }
    """

    authentication_classes = []  # w tym flow nie używamy JWT
    permission_classes = []

    def post(self, request, election_id: int):
        pesel = (request.data.get("pesel") or "").strip()
        code = (request.data.get("code") or "").strip()

        if len(pesel) != 11 or not pesel.isdigit():
            return Response({"detail": "Invalid PESEL"}, status=400)

        try:
            election = Election.objects.get(pk=election_id)
        except Election.DoesNotExist:
            return Response({"detail": "Election not found"}, status=404)

        now = timezone.now()
        if not (election.start_date <= now <= election.end_date):
            return Response({"detail": "Election is not active"}, status=400)

        try:
            voter = Voter.objects.get(election=election, pesel=pesel)
        except Voter.DoesNotExist:
            return Response({"detail": "Voter not found"}, status=404)

        if voter.verification_code != code:
            return Response({"detail": "Invalid code"}, status=400)

        if voter.has_voted:
            return Response({"detail": "Already voted"}, status=400)

        # wygeneruj portfel (web3.py, nie Metamask)
        acct = Account.create()
        eth_address = acct.address
        priv_encrypted = encrypt_bytes(acct.key)  # acct.key = bytes

        # sesja (20 min)
        session = VerificationSession.objects.create(
            election=election,
            voter=voter,
            eth_address=eth_address,
            privkey_encrypted=priv_encrypted,
            expires_at=now + timedelta(minutes=20),
        )

        # można od razu oznaczyć voter.is_authenticated=True (opcjonalnie)
        voter.is_authenticated = True
        voter.save(update_fields=["is_authenticated"])

        return Response(
            {"session_id": str(session.id), "eth_address": eth_address}, status=200
        )
