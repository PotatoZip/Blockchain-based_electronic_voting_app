require("dotenv").config();
const { ethers } = require("ethers");

// 1. Provider
const provider = new ethers.providers.JsonRpcProvider(`https://eth-sepolia.g.alchemy.com/v2/${process.env.ALCHEMY_API_KEY}`);

// 2. Tworzymy portfel
const wallet = ethers.Wallet.createRandom();

console.log("📬 Adres publiczny:", wallet.address);
console.log("🔐 Klucz prywatny:", wallet.privateKey);

// 3. Łączymy portfel z providerem
const connectedWallet = wallet.connect(provider);

// 4. Pobieramy saldo
async function checkBalance() {
    const balance = await connectedWallet.getBalance();
    console.log("💰 Saldo:", ethers.utils.formatEther(balance), "ETH");
}

checkBalance();
