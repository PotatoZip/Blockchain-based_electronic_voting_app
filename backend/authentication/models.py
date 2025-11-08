from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid


class Election(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Choice(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    election = models.ForeignKey(
        Election, on_delete=models.CASCADE, related_name="choices"
    )


class Voter(models.Model):
    pesel = models.CharField(max_length=11)
    verification_code = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    election = models.ForeignKey(
        Election, on_delete=models.CASCADE, related_name="voters"
    )
    is_authenticated = models.BooleanField(default=False)
    has_voted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("pesel", "election")


class VotingSession(models.Model):
    session_id = models.CharField(max_length=64, unique=True)  # uuid4 hex
    pesel = models.CharField(max_length=11)
    email = models.CharField(max_length=200, blank=True, null=True)
    election_id = models.IntegerField()
    public_address = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    has_voted = models.BooleanField(default=False)

    # anty-replay dla podpisów użytkownika
    next_nonce = models.BigIntegerField(default=1)

    def is_expired(self) -> bool:
        # przykładowo 2h
        return (timezone.now() - self.created_at).total_seconds() > 2 * 3600


class AuthChallenge(models.Model):
    address = models.CharField(max_length=64, db_index=True)
    nonce = models.CharField(max_length=128)
    expires_at = models.DateTimeField(db_index=True)

    @classmethod
    def purge_expired(cls):
        cls.objects.filter(expires_at__lt=timezone.now()).delete()
