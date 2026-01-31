# Blockchain-based Electronic Voting App

A secure, transparent electronic voting system built on Ethereum blockchain with Django backend and Vue.js frontend. Project created as part of a thesis in Computer Science at the Cracow University of Technology.

## Features

- 🔐 Secure wallet-based authentication with challenge-response protocol
- ⛓️ Blockchain-backed vote recording for transparency and immutability
- 🎭 Voter anonymization using cryptographic hashing with secret salt
- 🔄 Relayer pattern for gas-less voting (backend pays transaction fees)
- 📊 Real-time results fetching from smart contract
- 🛡️ Anti-replay protection with session-based nonces

## Architecture

- **Frontend**: Vue.js 3 + TypeScript + ethers.js
- **Backend**: Django 4.x + DRF + Web3.py
- **Blockchain**: Ethereum (Sepolia testnet) via Alchemy RPC
- **Smart Contract**: Solidity (ElectionManager.sol)

## Installation

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.10+ (for local backend development)

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/PotatoZip/Blockchain-based_electronic_voting_app.git
cd Blockchain-based_electronic_voting_app

# Start all services
docker compose up --build
```


## Management Commands

The backend provides several Django management commands for administration and debugging:

#### Check Transaction Status
```bash
python manage.py check_tx <tx_hash>
```

#### Check Voter Status
```bash
python manage.py check_voted <pesel> <election_id> [--show-key]
```

#### Get Election Results
```bash
python manage.py get_results <election_id> [--json] [--verbose]
```

#### Import Voters from CSV
```bash
python manage.py voters_csv_import
```

## Development

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Blockchain Setup
```bash
cd blockchain
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network sepolia
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) license.
