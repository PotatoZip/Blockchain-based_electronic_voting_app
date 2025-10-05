from django.db import models


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
