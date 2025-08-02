from django.contrib import admin
from .models import Election, Choice, Voter

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "start_date", "end_date")

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "election")

@admin.register(Voter)
class VoterAdmin(admin.ModelAdmin):
    list_display = ("pesel", "verification_code", "email", "election", "is_authenticated", "has_voted")