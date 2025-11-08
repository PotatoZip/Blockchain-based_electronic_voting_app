import os, json
from web3 import Web3
from eth_account import Account
from django.conf import settings
from eth_utils import keccak, to_hex

RPC = f"https://eth-sepolia.g.alchemy.com/v2/{os.environ['ALCHEMY_API_KEY']}"
w3 = Web3(Web3.HTTPProvider(RPC))

CONTRACT_ADDR = Web3.to_checksum_address(os.environ["CONTRACT_ADDRESS"])
RELAYER_PK = os.environ["DEPLOYER_PRIVATE_KEY"]
relayer = Account.from_key(RELAYER_PK)

ABI_PATH = os.path.join(settings.BASE_DIR, "abi", "ElectionManager.json")
with open(ABI_PATH, "r") as f:
    ABI = json.load(f)["abi"]

contract = w3.eth.contract(address=CONTRACT_ADDR, abi=ABI)


def voter_key(pesel: str, election_id: int, salt: str) -> str:
    return to_hex(keccak(text=f"{pesel}:{election_id}:{salt}"))


def has_voted_onchain(voter_key_hex: str) -> bool:
    return contract.functions.hasVoted(voter_key_hex).call()


def mark_voted_and_count(election_id: int, voter_key_hex: str, choice_id: int) -> str:
    nonce = w3.eth.get_transaction_count(relayer.address)
    tx = contract.functions.markVotedAndCount(
        election_id, voter_key_hex, choice_id
    ).build_transaction(
        {
            "from": relayer.address,
            "nonce": nonce,
            "gas": 250_000,
            "maxFeePerGas": w3.to_wei("15", "gwei"),
            "maxPriorityFeePerGas": w3.to_wei("1.5", "gwei"),
            "chainId": 11155111,  # Sepolia
        }
    )
    signed = relayer.sign_transaction(tx)
    if hasattr(signed, "rawTransaction"):
        raw = signed.rawTransaction
    elif hasattr(signed, "raw_transaction"):
        raw = signed.raw_transaction
    else:
        # Provide a helpful error if neither attribute is present
        raise AttributeError(
            "Signed transaction has no rawTransaction/raw_transaction attribute; check web3/eth-account versions"
        )

    tx_hash = w3.eth.send_raw_transaction(raw)
    return tx_hash.hex()
