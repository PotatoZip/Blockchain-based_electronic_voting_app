"""Admin configuration for the authentication app

Registers models with the Django admin interface and customizes their display and filtering options
"""

from django.contrib import admin
from .models import Election, Choice, Voter, VotingSession, AuthChallenge


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    search_fields = ("name",)
    list_filter = ("start_date", "end_date")
    date_hierarchy = "start_date"


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("name", "election")
    search_fields = ("name",)
    list_filter = ("election",)


@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ("pesel", "email", "election", "is_authenticated", "has_voted")
    search_fields = ("pesel", "email")
    list_filter = ("election", "is_authenticated", "has_voted")


@admin.register(VotingSession)
class VotingSessionAdmin(admin.ModelAdmin):
    list_display = (
        "session_id",
        "pesel",
        "election_id",
        "public_address",
        "is_verified",
        "has_voted",
        "created_at",
    )
    search_fields = ("session_id", "pesel", "public_address")
    list_filter = ("is_verified", "has_voted")
    readonly_fields = ("created_at",)


@admin.register(AuthChallenge)
class AuthChallengeAdmin(admin.ModelAdmin):
    list_display = ("address", "expires_at")
    search_fields = ("address",)
    list_filter = ("expires_at",)
