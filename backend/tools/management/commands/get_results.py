"""Get election results from blockchain and display them"""

import json
from django.core.management.base import BaseCommand, CommandError
from authentication.models import Election
from authentication.client import contract


class Command(BaseCommand):
    help = "Get election results from blockchain"

    def add_arguments(self, parser):
        parser.add_argument(
            "election_id", type=int, help="Election ID to get results for"
        )
        parser.add_argument(
            "--json", action="store_true", help="Output results as JSON"
        )
        parser.add_argument(
            "--verbose", action="store_true", help="Show detailed information"
        )

    def handle(self, *args, **options):
        election_id = options["election_id"]
        as_json = options["json"]
        verbose = options["verbose"]

        try:
            election = Election.objects.get(pk=election_id)
        except Election.DoesNotExist:
            raise CommandError(f"Election with ID {election_id} not found")

        choices = list(election.choices.all())

        if not choices:
            self.stdout.write(
                self.style.WARNING(f"No choices found for election #{election_id}")
            )
            return

        results = []
        total_votes = 0

        for choice in choices:
            try:
                count = contract.functions.getChoiceCount(election_id, choice.id).call()
            except Exception as e:
                raise CommandError(f"Failed to get count for choice {choice.id}: {e}")

            results.append(
                {"choice_id": choice.id, "name": choice.name, "votes": count}
            )
            total_votes += count

        if as_json:
            output = {
                "election_id": election_id,
                "election_name": election.name,
                "total_votes": total_votes,
                "results": results,
            }
            self.stdout.write(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
            self.stdout.write(
                self.style.SUCCESS(f"Election: {election.name} (ID: {election_id})")
            )
            self.stdout.write(self.style.SUCCESS(f'{"="*60}\n'))

            if verbose:
                self.stdout.write(f"Start Date: {election.start_date}")
                self.stdout.write(f"End Date: {election.end_date}")
                self.stdout.write(f"Total Votes: {total_votes}\n")

            for result in results:
                percentage = (
                    (result["votes"] / total_votes * 100) if total_votes > 0 else 0
                )
                bar_length = int(percentage / 2)
                bar = "█" * bar_length + "░" * (50 - bar_length)

                self.stdout.write(
                    f"{result['name']:<30} {result['votes']:>5} votes  {percentage:>5.1f}%"
                )
                if verbose:
                    self.stdout.write(f"  {bar}")

            self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
            self.stdout.write(f"Total votes cast: {total_votes}")
            self.stdout.write(self.style.SUCCESS(f'{"="*60}\n'))
