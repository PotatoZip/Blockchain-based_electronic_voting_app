import sys, json, os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "voting_app.settings")
import django

django.setup()
from authentication.models import Election
from authentication.client import contract

if len(sys.argv) < 2:
    print("Usage: python get_results.py <election_id>")
    sys.exit(2)

eid = int(sys.argv[1])
try:
    el = Election.objects.get(pk=eid)
except Election.DoesNotExist:
    print(json.dumps({"error": "Election not found", "election": eid}))
    sys.exit(1)

choices = [{"id": c.id, "name": c.name} for c in el.choices.all()]
res = []
for c in choices:
    try:
        cnt = contract.functions.getChoiceCount(eid, c["id"]).call()
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
    res.append({"choice_id": c["id"], "name": c["name"], "votes": cnt})

print(json.dumps({"election": eid, "results": res}, ensure_ascii=False))
