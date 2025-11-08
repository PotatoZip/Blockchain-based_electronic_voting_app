from django.core.mail import send_mass_mail
from django.template import Template, Context
from authentication.models import Election
import os

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "basic_mail_template.txt")

with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    email_template = f.read()


def send_test_mail(election_id):
    election = Election.objects.get(id=election_id)
    voters = election.voters.all()
    messages = []

    for voter in voters:
        template = Template(email_template)
        context = Context({"election": election, "voter": voter})

        subject = f"Invitation for: { election.name }"
        message = template.render(context)

        messages.append((subject, message, None, [voter.email]))
    # send_mass_mail returns the number of messages sent
    sent_count = send_mass_mail(messages, fail_silently=False)
    return sent_count
