const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Protocolo NatyWeb3", function () {
  let NatyToken, NatyNFT, NatyStaking, NatyDAO, MockOracle;
  let token, nft, staking, dao, oracle;
  let owner, user1, user2;

  beforeEach(async function () {
    [owner, user1, user2] = await ethers.getSigners();

    // Deploy Mock Oracle (ETH Price = $3000)
    const MockOracleFactory = await ethers.getContractFactory("MockV3Aggregator");
    oracle = await MockOracleFactory.deploy(300000000000n); // 8 decimals

    // Deploy NatyToken
    const TokenFactory = await ethers.getContractFactory("NatyToken");
    token = await TokenFactory.deploy(owner.address);

    // Deploy NatyNFT
    const NFTFactory = await ethers.getContractFactory("NatyNFT");
    nft = await NFTFactory.deploy(owner.address);

    // Deploy Staking
    const StakingFactory = await ethers.getContractFactory("NatyStaking");
    staking = await StakingFactory.deploy(
      token.target,
      token.target,
      oracle.target,
      owner.address
    );

    // Deploy DAO
    const DAOFactory = await ethers.getContractFactory("NatyDAO");
    dao = await DAOFactory.deploy(staking.target, owner.address);

    // Transfer some tokens to users
    await token.transfer(user1.address, ethers.parseEther("1000"));
    await token.transfer(user2.address, ethers.parseEther("1000"));
  });

  describe("NatyToken", function () {
    it("Deve ter o nome e símbolo corretos", async function () {
      expect(await token.name()).to.equal("NatyToken");
      expect(await token.symbol()).to.equal("NATY");
    });
  });

  describe("Staking e Oráculo", function () {
    it("Deve permitir stake de tokens", async function () {
      const amount = ethers.parseEther("100");
      await token.connect(user1).approve(staking.target, amount);
      await staking.connect(user1).stake(amount);

      expect(await staking.balanceOf(user1.address)).to.equal(amount);
      expect(await staking.totalSupply()).to.equal(amount);
    });

    it("Deve calcular recompensas baseado no preço do oráculo", async function () {
      const amount = ethers.parseEther("100");
      await token.connect(user1).approve(staking.target, amount);
      await staking.connect(user1).stake(amount);

      // Passar o tempo
      await ethers.provider.send("evm_increaseTime", [3600]); // 1 hora
      await ethers.provider.send("evm_mine");

      const reward = await staking.earned(user1.address);
      expect(reward).to.be.gt(0);
    });
  });

  describe("NatyDAO", function () {
    it("Deve permitir criar propostas e votar", async function () {
      // Stake para ter poder de voto
      const amount = ethers.parseEther("100");
      await token.connect(user1).approve(staking.target, amount);
      await staking.connect(user1).stake(amount);

      await dao.connect(user1).createProposal("Melhorar a Naty!");
      await dao.connect(user1).vote(0);

      const proposal = await dao.proposals(0);
      expect(proposal.voteCount).to.equal(amount);
    });

    it("Não deve permitir votar sem stake", async function () {
      await dao.connect(user2).createProposal("Voto sem stake");
      await expect(dao.connect(user2).vote(0)).to.be.revertedWith("No voting power (stake tokens first)");
    });
  });
});
