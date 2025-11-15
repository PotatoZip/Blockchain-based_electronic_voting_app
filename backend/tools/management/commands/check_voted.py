from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from authentication.client import contract, voter_key


class Command(BaseCommand):
    help = 'Check if a voter has voted on-chain for a specific election'

    def add_arguments(self, parser):
        parser.add_argument(
            'pesel',
            type=str,
            help='PESEL number of the voter'
        )
        parser.add_argument(
            'election_id',
            type=int,
            help='Election ID to check'
        )
        parser.add_argument(
            '--show-key',
            action='store_true',
            help='Display the voter_key hash (for debugging)'
        )

    def handle(self, *args, **options):
        pesel = options['pesel']
        election_id = options['election_id']
        show_key = options['show_key']

        try:
            salt = settings.SECRET_SALT
        except AttributeError:
            raise CommandError('SECRET_SALT not found in settings')

        # Generate voter_key
        vk = voter_key(pesel, election_id, salt)

        if show_key:
            self.stdout.write(f'Voter Key: {vk}')

        try:
            has_voted = contract.functions.hasVoted(vk).call()
        except Exception as e:
            raise CommandError(f'Failed to check voting status: {e}')

        if has_voted:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Voter has VOTED in election #{election_id}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'✗ Voter has NOT voted in election #{election_id}')
            )
