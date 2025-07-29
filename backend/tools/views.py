from django.shortcuts import render
from django.http import HttpResponse
from .mailing.email_test import send_test_mail

def send_test_view(request, voting_id):
    send_test_mail(voting_id)
    return HttpResponse(f"Emails sent to {voting_id}")