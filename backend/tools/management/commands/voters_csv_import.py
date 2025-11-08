from django.core.management.base import BaseCommand, CommandError
from authentication.models import Voter, Election

import csv
import random
import string


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--voting-id", type=int, required=True)
        parser.add_argument("--csv", type=str, required=True)
        parser.add_argument(
            "--update-existing",
            action="store_true",
            help="Update email/verification_code for existing voter for this election",
        )

    def handle(self, *args, **options):
        voting_id = options["voting_id"]
        csv_path = options["csv"]

        try:
            voting = Election.objects.get(pk=voting_id)
        except Election.DoesNotExist:
            raise CommandError(f"Election with id {voting_id} does not exist")

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pesel = row["pesel"].strip()
                email = row.get("email", "").strip()
                verification_code = self.generate_code()

                voter, created = Voter.objects.get_or_create(
                    pesel=pesel,
                    election=voting,
                    defaults={
                        "email": email,
                        "verification_code": verification_code,
                    },
                )

                if created:
                    self.stdout.write(
                        f"Voter added: {email} (pesel {pesel}) to election {voting.id}"
                    )
                else:
                    if options.get("update_existing"):
                        # update allowed fields
                        voter.email = email or voter.email
                        voter.verification_code = (
                            verification_code or voter.verification_code
                        )
                        voter.save()
                        self.stdout.write(
                            f"Voter updated: {email} (pesel {pesel}) for election {voting.id}"
                        )
                    else:
                        self.stdout.write(
                            f"Voter already exists for this election: {email} (pesel {pesel})"
                        )

    def generate_code(self):
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
