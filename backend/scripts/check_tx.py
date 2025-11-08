import sys, os

# Ensure Django settings are configured when running this script standalone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voting_app.settings")
import django

django.setup()

from authentication.client import w3


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_tx.py <tx_hash>")
        sys.exit(2)
    h = sys.argv[1]
    try:
        r = w3.eth.get_transaction_receipt(h)
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)
    out = {
        "status": getattr(r, "status", None),
        "blockNumber": getattr(r, "blockNumber", None),
        "transactionIndex": getattr(r, "transactionIndex", None),
        "gasUsed": getattr(r, "gasUsed", None),
        "logs_count": len(getattr(r, "logs", [])),
    }
    print(out)


if __name__ == "__main__":
    main()
