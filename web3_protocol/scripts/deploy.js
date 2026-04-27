const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Iniciando deploy com a conta:", deployer.address);

  // 1. Deploy NatyToken
  console.log("Realizando deploy do NatyToken...");
  const NatyToken = await hre.ethers.deployContract("NatyToken", [deployer.address]);
  await NatyToken.waitForDeployment();
  console.log("NatyToken implantado em:", NatyToken.target);

  // 2. Deploy NatyNFT
  console.log("Realizando deploy do NatyNFT...");
  const NatyNFT = await hre.ethers.deployContract("NatyNFT", [deployer.address]);
  await NatyNFT.waitForDeployment();
  console.log("NatyNFT implantado em:", NatyNFT.target);

  // 3. Deploy NatyStaking
  // Endereço do Oráculo ETH/USD na Sepolia: 0x694AA1769357215DE4FAC081bf1f309aDC325306
  const SEPOLIA_ORACLE = "0x694AA1769357215DE4FAC081bf1f309aDC325306";
  console.log("Realizando deploy do NatyStaking...");
  const NatyStaking = await hre.ethers.deployContract("NatyStaking", [
    NatyToken.target,
    NatyToken.target,
    SEPOLIA_ORACLE,
    deployer.address
  ]);
  await NatyStaking.waitForDeployment();
  console.log("NatyStaking implantado em:", NatyStaking.target);

  // 4. Deploy NatyDAO
  console.log("Realizando deploy do NatyDAO...");
  const NatyDAO = await hre.ethers.deployContract("NatyDAO", [
    NatyStaking.target,
    deployer.address
  ]);
  await NatyDAO.waitForDeployment();
  console.log("NatyDAO implantado em:", NatyDAO.target);

  console.log("\n--- DEPLOY CONCLUÍDO COM SUCESSO ---");
  console.log("NatyToken:", NatyToken.target);
  console.log("NatyNFT:", NatyNFT.target);
  console.log("NatyStaking:", NatyStaking.target);
  console.log("NatyDAO:", NatyDAO.target);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
