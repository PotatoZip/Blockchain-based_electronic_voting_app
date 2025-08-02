from django.core.management.base import BaseCommand, CommandError
from authentication.models import Voter, Election

import csv
import random
import string

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--voting-id', type=int, required=True)
        parser.add_argument('--csv', type=str, required=True)

    def handle(self, *args, **options):
        voting_id = options['voting_id']
        csv_path = options['csv']

        try:
            voting = Election.objects.get(pk=voting_id)
        except Election.DoesNotExist:
            raise CommandError(f"Election with id {voting_id} does not exist")
        
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pesel = row['pesel'].strip()
                email=row.get('email', '').strip()
                verification_code=self.generate_code()

                voter, created = Voter.objects.get_or_create(
                    pesel=pesel,
                    defaults={
                        'email':email,
                        'verification_code':verification_code,
                        'election':voting
                    }
                )

                if created:
                    self.stdout.write(f"Voter add succes: {email}")
                else:
                    self.stdout.write(f"Voter add fail: {email}")

    def generate_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))