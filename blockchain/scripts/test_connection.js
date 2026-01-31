require("dotenv").config();
const ethers = require("ethers");

async function main() {
  const url = `https://eth-sepolia.g.alchemy.com/v2/${process.env.ALCHEMY_API_KEY}`;
  const provider = new ethers.JsonRpcProvider(url);

  const net = await provider.getNetwork();
  const block = await provider.getBlockNumber();

  console.log("Network:", net.name, "chainId:", Number(net.chainId));
  console.log("Latest block:", block);
}

main().catch(console.error);
