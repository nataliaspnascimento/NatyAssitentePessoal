# Protocolo NatyWeb3 - Fase 2 Avançada 🚀

Este repositório contém a implementação completa de um MVP de Protocolo Web3, incluindo Tokens, NFTs, Staking com Oráculo e Governança DAO.

## 📑 Relatórios e Documentação
- [Relatório Técnico Profissional](./web3_protocol/relatorio_final.md)
- [Auditoria de Segurança](./web3_protocol/auditoria_seguranca.md)
- [Modelagem e Arquitetura](./web3_protocol/modelagem.md)

## 🏗️ Estrutura do Projeto
- `/contracts`: Smart Contracts em Solidity.
- `/frontend`: Interface React + Vite integrada.
- `/scripts`: Scripts de deploy e automação.
- `naty_apresentacao.py`: Script de Assistente de Voz para apresentação.

## 🔗 Endereços de Deploy (Sepolia Testnet)
- **NatyToken:** `0x914D662e1C1691E2701e44C6468Bf0E0757fFe88`
- **NatyNFT:** `0xe31b75F44bf2843c57C0865f6A0f28b5fDe00AcE`
- **NatyStaking:** `0x8c7e68221e702134B712Bac7ae4d156BB940f761`
- **NatyDAO:** `0xD61de862E3adc79648b55A67681A7118548fD86C`

## 🚀 Como Iniciar

### 1. Requisitos
- Node.js e NPM instalados.
- Python 3.x (para a assistente Naty).
- Carteira MetaMask com Sepolia ETH.

### 2. Rodar o Frontend
```bash
cd web3_protocol/frontend
npm install
npm run dev
```
Acesse: `http://localhost:5174`

### 3. Iniciar a Assistente Naty (Opcional para vídeo)
```bash
pip install -r requirements.txt
python web3_protocol/naty_apresentacao.py
```
*Diga: "Naty, fale sobre o projeto" para iniciar a explicação por voz.*

## 📽️ Guia para Apresentação
1. Abra o Frontend e clique em **"Abrir Teleprompter"** para ter o script na tela.
2. Inicie a gravação e dê o comando de voz para a Naty.
3. Demonstre o fluxo: **Pedir 100 NATY -> Mintar NFT -> Fazer Stake -> Criar Proposta.**

---
Desenvolvido por Natália Nascimento em parceria com NATY Assistente.
