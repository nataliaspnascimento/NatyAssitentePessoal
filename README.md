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

### 3. Iniciar a Assistente Naty
Basta utilizar o arquivo na raiz do projeto:
```bash
./INICIAR_NATY.bat
```
*Diga: "Naty, apresente o relatório técnico NatyWeb3" para a Naty começar a explicar por voz.*

## 📽️ Guia para Apresentação
1. Ao rodar o script `.bat`, duas abas abrirão no seu navegador: O **Frontend (dApp)** e o **Teleprompter Studio**.
2. Abra o **Studio** em um segundo monitor (ou deixe no fundo) para ler o roteiro, gravar a tela e acompanhar os comandos.
3. No vídeo, inicie a gravação (direto no Studio ou no OBS) e dê o comando de voz para a Naty.
4. Enquanto ela fala, alterne para a aba do Frontend e demonstre o fluxo: **Pedir 100 NATY -> Mintar NFT -> Fazer Stake -> Criar Proposta.**

---
Desenvolvido por Natália Nascimento em parceria com NATY Assistente.
