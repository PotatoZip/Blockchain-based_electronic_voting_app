from django.shortcuts import render
from django.http import HttpResponse
from .mailing.email_test import send_test_mail


def send_test_view(request, voting_id):
    try:
        sent_count = send_test_mail(voting_id)
    except Exception as e:
        # Return error details so caller can see what went wrong (useful during dev)
        return HttpResponse(f"Error sending emails for {voting_id}: {e}", status=500)

    return HttpResponse(f"Emails sent to {voting_id}. Count: {sent_count}")
