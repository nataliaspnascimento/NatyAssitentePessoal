import React, { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import { Wallet, Coins, Rocket, Vote, ShieldCheck, Zap, ExternalLink } from 'lucide-react';
import { NATY_TOKEN_ABI, NATY_NFT_ABI, NATY_STAKING_ABI, NATY_DAO_ABI } from './contracts/abis';

// Endereços Reais (Deploy Sepolia)
const NATY_TOKEN_ADDRESS = "0x914D662e1C1691E2701e44C6468Bf0E0757fFe88";
const NATY_NFT_ADDRESS = "0xe31b75F44bf2843c57C0865f6A0f28b5fDe00AcE";
const NATY_STAKING_ADDRESS = "0x8c7e68221e702134B712Bac7ae4d156BB940f761";
const NATY_DAO_ADDRESS = "0xD61de862E3adc79648b55A67681A7118548fD86C";

function App() {
  const [account, setAccount] = useState(null);
  const [balance, setBalance] = useState("0");
  const [stakedBalance, setStakedBalance] = useState("0");
  const [rewards, setRewards] = useState("0");
  const [loading, setLoading] = useState(false);
  const [stakeAmount, setStakeAmount] = useState("");
  const [proposalDesc, setProposalDesc] = useState("");
  const [showTeleprompter, setShowTeleprompter] = useState(false);

  const teleprompterText = [
    "Olá! Eu sou a Naty, sua assistente pessoal.",
    "Neste projeto da Fase 2 Avançada, desenvolvemos um Protocolo Web3 completo.",
    "O ecossistema conta com o NatyToken (ERC-20), NatyNFT (ERC-721),",
    "um sistema de Staking com recompensas via Oráculo Chainlink e uma DAO.",
    "Todos os contratos foram implantados na rede Sepolia e auditados.",
    "Vamos agora demonstrar o fluxo de Mint, Stake e Votação ao vivo."
  ];

  useEffect(() => {
    if (account) {
      updateBalances();
    }
  }, [account]);

  const connectWallet = async () => {
    if (window.ethereum) {
      try {
        const provider = new ethers.BrowserProvider(window.ethereum);
        const accounts = await provider.send("eth_requestAccounts", []);
        setAccount(accounts[0]);
      } catch (error) {
        console.error("Erro ao conectar carteira:", error);
      }
    } else {
      alert("Por favor, instale a MetaMask!");
    }
  };

  const updateBalances = async () => {
    try {
      const provider = new ethers.BrowserProvider(window.ethereum);
      const tokenContract = new ethers.Contract(NATY_TOKEN_ADDRESS, NATY_TOKEN_ABI, provider);
      const stakingContract = new ethers.Contract(NATY_STAKING_ADDRESS, NATY_STAKING_ABI, provider);

      const bal = await tokenContract.balanceOf(account);
      const staked = await stakingContract.balanceOf(account);
      const earned = await stakingContract.earned(account);

      setBalance(ethers.formatEther(bal));
      setStakedBalance(ethers.formatEther(staked));
      setRewards(ethers.formatEther(earned));
    } catch (error) {
      console.error("Erro ao carregar saldos:", error);
    }
  };

  const handleStake = async () => {
    if (!stakeAmount || isNaN(stakeAmount)) return;
    try {
      setLoading(true);
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      
      const tokenContract = new ethers.Contract(NATY_TOKEN_ADDRESS, NATY_TOKEN_ABI, signer);
      const stakingContract = new ethers.Contract(NATY_STAKING_ADDRESS, NATY_STAKING_ABI, signer);

      const amount = ethers.parseEther(stakeAmount);
      
      // 1. Approve
      const approveTx = await tokenContract.approve(NATY_STAKING_ADDRESS, amount);
      await approveTx.wait();
      
      // 2. Stake
      const stakeTx = await stakingContract.stake(amount);
      await stakeTx.wait();

      alert("Stake realizado com sucesso!");
      updateBalances();
    } catch (error) {
      console.error(error);
      alert("Erro ao realizar stake.");
    } finally {
      setLoading(false);
    }
  };

  const handleMintNFT = async () => {
    try {
      setLoading(true);
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      const nftContract = new ethers.Contract(NATY_NFT_ADDRESS, NATY_NFT_ABI, signer);

      const tx = await nftContract.safeMint(account, "ipfs://QmPlaceholder");
      await tx.wait();
      alert("NFT Mintado com Sucesso!");
    } catch (error) {
      console.error(error);
      alert("Erro ao mintar NFT.");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProposal = async () => {
    if (!proposalDesc) return;
    try {
      setLoading(true);
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      const daoContract = new ethers.Contract(NATY_DAO_ADDRESS, NATY_DAO_ABI, signer);

      const tx = await daoContract.createProposal(proposalDesc);
      await tx.wait();
      alert("Proposta enviada à DAO!");
      setProposalDesc("");
    } catch (error) {
      console.error(error);
      alert("Erro ao criar proposta.");
    } finally {
      setLoading(false);
    }
  };

  const handleRequestTokens = async () => {
    try {
      setLoading(true);
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      const tokenContract = new ethers.Contract(NATY_TOKEN_ADDRESS, NATY_TOKEN_ABI, signer);

      const tx = await tokenContract.mint(account, ethers.parseEther("100"));
      await tx.wait();
      alert("100 NATY creditados com sucesso!");
      updateBalances();
    } catch (error) {
      console.error(error);
      alert("Erro ao solicitar tokens.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <div className="logo">NATY PROTOCOL</div>
        <div style={{display: 'flex', gap: '15px', alignItems: 'center', justifyContent: 'flex-end', flex: 1}}>
          {account && (
            <button className="btn btn-outline" onClick={handleRequestTokens} disabled={loading} style={{ padding: '0.5rem 1rem', fontSize: '0.9rem', borderRadius: '20px' }}>
              Pedir 100 NATY
            </button>
          )}
          <button onClick={connectWallet} style={{ 
            display: 'flex', alignItems: 'center', gap: '10px', 
            background: account ? 'rgba(16, 185, 129, 0.15)' : 'rgba(244, 63, 94, 0.15)', 
            color: account ? '#10b981' : '#f43f5e', 
            border: `1px solid ${account ? '#10b981' : '#f43f5e'}`,
            padding: '0.6rem 1.2rem', fontSize: '0.95rem', borderRadius: '30px',
            cursor: 'pointer', fontWeight: 'bold', transition: '0.3s'
          }}>
            <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: account ? '#10b981' : '#f43f5e', boxShadow: `0 0 10px ${account ? '#10b981' : '#f43f5e'}` }}></div>
            {account ? `Conectado: ${account.substring(0, 6)}...${account.substring(38)}` : "Não Conectado (Clique aqui)"}
          </button>
        </div>
      </header>

      <section className="glass-card" style={{marginBottom: '3rem', textAlign: 'center', background: 'linear-gradient(rgba(30,41,59,0.7), rgba(139,92,246,0.1))'}}>
        <div className="badge">Fase 2: Avançada | Sepolia Testnet</div>
        <h1 style={{fontSize: '3rem', marginBottom: '1rem'}}>O Futuro Descentralizado da Naty</h1>
        <p style={{color: 'var(--text-dim)', maxWidth: '600px', margin: '0 auto'}}>
          Faça stake de seus tokens NATY, ganhe recompensas dinâmicas e participe da governança.
        </p>
      </section>

      <div className="grid">
        <div className="glass-card">
          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
            <h3>Painel de Ativos</h3>
            <Coins color="var(--accent)" />
          </div>
          <div style={{marginBottom: '1.2rem'}}>
            <p className="stat-label">Saldo Disponível</p>
            <p className="stat-value">{parseFloat(balance).toFixed(4)} <span style={{fontSize: '0.8rem', color: 'var(--primary)'}}>NATY</span></p>
          </div>
          <div style={{marginBottom: '1.2rem'}}>
            <p className="stat-label">Total em Stake</p>
            <p className="stat-value">{parseFloat(stakedBalance).toFixed(4)} <span style={{fontSize: '0.8rem', color: 'var(--secondary)'}}>NATY</span></p>
          </div>
          <div>
            <p className="stat-label">Recompensas Acumuladas</p>
            <p className="stat-value" style={{color: 'var(--accent)'}}>{parseFloat(rewards).toFixed(6)} <span style={{fontSize: '0.8rem'}}>NATY</span></p>
          </div>
        </div>

        <div className="glass-card">
          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
            <h3>Staking & Oráculo</h3>
            <Zap color="var(--primary)" />
          </div>
          <p style={{fontSize: '0.9rem', color: 'var(--text-dim)'}}>Recompensas ajustadas pelo preço ETH/USD via Chainlink.</p>
          <input 
            type="number" 
            placeholder="Quantidade NATY" 
            value={stakeAmount}
            onChange={(e) => setStakeAmount(e.target.value)}
          />
          <button className="btn" style={{width: '100%'}} onClick={handleStake} disabled={loading || !account}>
            {loading ? "Processando..." : "Realizar Stake"}
          </button>
          <div style={{marginTop: '1rem', display: 'flex', gap: '10px'}}>
             <button className="btn btn-outline" style={{flex: 1}} onClick={updateBalances}>Atualizar</button>
             <a href={`https://sepolia.etherscan.io/address/${NATY_STAKING_ADDRESS}`} target="_blank" className="btn btn-outline" style={{padding: '0.75rem', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                <ExternalLink size={18} />
             </a>
          </div>
        </div>

        <div className="glass-card">
          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
            <h3>NFT Rewards</h3>
            <Rocket color="var(--secondary)" />
          </div>
          <div style={{background: 'rgba(0,0,0,0.2)', height: '120px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem'}}>
             <ShieldCheck size={48} color="rgba(255,255,255,0.2)" className={loading ? "animate-pulse" : ""} />
          </div>
          <button className="btn btn-outline" style={{width: '100%'}} onClick={handleMintNFT} disabled={loading || !account}>
            {loading ? "Mintando..." : "Mintar NFT Exclusivo"}
          </button>
        </div>

        <div className="glass-card" style={{gridColumn: '1 / -1'}}>
          <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem'}}>
            <h3>NatyDAO Governança</h3>
            <Vote color="var(--accent)" />
          </div>
          <div style={{display: 'flex', gap: '1rem', alignItems: 'center'}}>
            <div style={{flex: 2}}>
              <input 
                type="text" 
                placeholder="Ex: 'Aumentar taxas de staking para 15%'" 
                value={proposalDesc}
                onChange={(e) => setProposalDesc(e.target.value)}
                style={{margin: 0}}
              />
            </div>
            <button className="btn" style={{flex: 1}} onClick={handleCreateProposal} disabled={loading || !account}>
              Criar Proposta
            </button>
          </div>
        </div>
      </div>

      <footer style={{marginTop: '4rem', textAlign: 'center', color: 'var(--text-dim)', fontSize: '0.8rem'}}>
        &copy; 2026 Naty Protocol - Implementado com Sucesso na Sepolia
      </footer>
    </div>
  );
}

export default App;
