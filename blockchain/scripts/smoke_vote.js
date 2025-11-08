// scripts/smoke_vote.js
require("dotenv").config();
const hre = require("hardhat");
const { ethers } = hre;

function voterKey(pesel, electionId, salt) {
  return ethers.keccak256(ethers.toUtf8Bytes(`${pesel}:${electionId}:${salt}`));
}

async function main() {
  const addr = process.env.CONTRACT_ADDRESS;
  if (!addr) throw new Error("Brak CONTRACT_ADDRESS w .env");

  const contract = await ethers.getContractAt("ElectionManager", addr);

  const electionId = 1;
  const choiceId = 2;
  const pesel = "12345678901";
  const salt = process.env.SECRET_SALT || "DEV_SALT";
  const key = voterKey(pesel, electionId, salt);

  console.log("Has voted before?:", await contract.hasVoted(key));

  const tx = await contract.markVotedAndCount(electionId, key, choiceId);
  console.log("tx sent:", tx.hash);
  await tx.wait();

  console.log("confirmed.");
  console.log("Now has voted?:", await contract.hasVoted(key));
  const count = await contract.getChoiceCount(electionId, choiceId);
  console.log("choice count:", count.toString());
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
