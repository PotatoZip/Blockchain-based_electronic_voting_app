require("dotenv").config();
const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deployer:", deployer.address);

  const Factory = await hre.ethers.getContractFactory("ElectionManager");
  const contract = await Factory.deploy(deployer.address);

  await contract.waitForDeployment();
  const address = await contract.getAddress();

  console.log("ElectionManager deployed at:", address);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
