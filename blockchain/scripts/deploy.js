// scripts/deploy.js
require("dotenv").config();
const hre = require("hardhat"); // daje Ci { ethers } w v6

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deployer:", deployer.address);

  const Factory = await hre.ethers.getContractFactory("ElectionManager");
  const contract = await Factory.deploy(deployer.address);

  await contract.waitForDeployment(); // v6
  const address = await contract.getAddress(); // v6

  console.log("ElectionManager deployed at:", address);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
