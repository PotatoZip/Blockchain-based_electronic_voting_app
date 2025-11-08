import sys
from authentication.client import contract, voter_key
from django.conf import settings

def main():
    if len(sys.argv) < 3:
        print('Usage: python check_voted.py <pesel> <election_id>')
        sys.exit(2)
    pesel = sys.argv[1]
    election_id = int(sys.argv[2])
    try:
        salt = settings.SECRET_SALT
    except Exception:
        salt = 'Super_Tajny_Sól_Do_Hashu'
    vk = voter_key(pesel, election_id, salt)
    try:
        res = contract.functions.hasVoted(vk).call()
        print(res)
    except Exception as e:
        print('ERROR:', e)
        sys.exit(1)

if __name__ == '__main__':
    main()
