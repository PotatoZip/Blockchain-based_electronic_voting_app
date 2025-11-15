from django.http import HttpResponse
from .mailing.email import send_mail


def send_view(request, voting_id):
    """View to send emails to voters of a specific election identified by voting_id"""
    try:
        sent_count = send_mail(voting_id)
    except Exception as e:
        return HttpResponse(f"Error sending emails for {voting_id}: {e}", status=500)

    return HttpResponse(f"Emails sent to {voting_id}. Count: {sent_count}")
