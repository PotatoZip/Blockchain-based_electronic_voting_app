// Copies the ElectionManager ABI artifact to the backend for Web3 integration
const fs = require("fs");
const path = require("path");

const SRC = path.resolve(
  __dirname,
  "..",
  "artifacts",
  "contracts",
  "ElectionManager.sol",
  "ElectionManager.json"
);
const DST = path.resolve(
  __dirname,
  "..",
  "..",
  "backend",
  "abi",
  "ElectionManager.json"
);

function main() {
  if (!fs.existsSync(SRC)) {
    console.error("ABI artifact not found at:", SRC);
    console.error("Have you run `npm run compile` or deployed the contract?");
    process.exit(1);
  }
  // Ensure destination dir exists
  const dstDir = path.dirname(DST);
  if (!fs.existsSync(dstDir)) {
    fs.mkdirSync(dstDir, { recursive: true });
  }
  fs.copyFileSync(SRC, DST);
  console.log("✅ ABI copied to", DST);
}

main();
