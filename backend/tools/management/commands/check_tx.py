from django.core.management.base import BaseCommand, CommandError
from authentication.client import w3


class Command(BaseCommand):
    help = 'Check transaction status on blockchain'

    def add_arguments(self, parser):
        parser.add_argument(
            'tx_hash',
            type=str,
            help='Transaction hash to check (e.g., 0xabc123...)'
        )

    def handle(self, *args, **options):
        tx_hash = options['tx_hash']
        
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
        except Exception as e:
            raise CommandError(f'Failed to get transaction receipt: {e}')

        self.stdout.write(self.style.SUCCESS('Transaction Receipt:'))
        self.stdout.write(f'  Status: {receipt.status} {"✓ Success" if receipt.status == 1 else "✗ Failed"}')
        self.stdout.write(f'  Block Number: {receipt.blockNumber}')
        self.stdout.write(f'  Transaction Index: {receipt.transactionIndex}')
        self.stdout.write(f'  Gas Used: {receipt.gasUsed}')
        self.stdout.write(f'  Logs Count: {len(receipt.logs)}')
        
        if receipt.logs:
            self.stdout.write(self.style.WARNING(f'\n  Events emitted: {len(receipt.logs)}'))
