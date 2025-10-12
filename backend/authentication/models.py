from django.db import models
from django.utils import timezone
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


class VerificationSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    election = models.ForeignKey(
        "Election", on_delete=models.CASCADE, related_name="verification_sessions"
    )
    voter = models.ForeignKey(
        "Voter", on_delete=models.CASCADE, related_name="verification_sessions"
    )
    eth_address = models.CharField(max_length=100)
    privkey_encrypted = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def is_valid(self) -> bool:
        return (not self.used) and (timezone.now() < self.expires_at)
