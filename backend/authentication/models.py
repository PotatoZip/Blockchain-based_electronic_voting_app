"""Models for the election system, including elections, choices, voters"""

from django.db import models
from django.utils import timezone


class Election(models.Model):
    """Model representing an election event"""

    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Choice(models.Model):
    """Model representing a choice/option in an election"""

    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    election = models.ForeignKey(
        Election, on_delete=models.CASCADE, related_name="choices"
    )


class Voter(models.Model):
    """Model representing a voter registered for an election"""

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
    """Model representing a voting session for a voter"""

    session_id = models.CharField(max_length=64, unique=True)
    pesel = models.CharField(max_length=11)
    email = models.CharField(max_length=200, blank=True, null=True)
    election_id = models.IntegerField()
    public_address = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    has_voted = models.BooleanField(default=False)
    next_nonce = models.BigIntegerField(default=1)

    def is_expired(self) -> bool:
        return (timezone.now() - self.created_at).total_seconds() > 3600


class AuthChallenge(models.Model):
    """Model representing an authentication challenge for a public address
    it is used to verify ownership of the address by signing the nonce
    """

    address = models.CharField(max_length=64, db_index=True)
    nonce = models.CharField(max_length=128)
    expires_at = models.DateTimeField(db_index=True)

    @classmethod
    def purge_expired(cls):
        cls.objects.filter(expires_at__lt=timezone.now()).delete()
