from voz.falar import falar
import time
import os
import re

def apresentar():
    caminho_relatorio = os.path.join("web3_protocol", "relatorio_final.md")
    
    if not os.path.exists(caminho_relatorio):
        falar("Desculpe, não consegui encontrar o arquivo relatorio final ponto md.")
        return "Arquivo não encontrado."

    with open(caminho_relatorio, "r", encoding="utf-8") as f:
        linhas = f.readlines()
        
    falar("Iniciando a leitura do relatório.")
    time.sleep(1)

    dentro_codigo = False
    
    for linha in linhas:
        linha = linha.strip()
        
        # Ignora blocos de código/mermaid
        if linha.startswith("```"):
            dentro_codigo = not dentro_codigo
            continue
        if dentro_codigo:
            continue
            
        # Ignora tabelas, divisórias, e código mermaid solto
        if not linha or linha.startswith("|") or linha.startswith("---") or linha.startswith("graph ") or "-->" in linha:
            continue

        # Ignora a frase final de observação
        if "Este documento serve como guia" in linha:
            continue

        # Limpeza de caracteres Markdown para leitura humana
        linha = re.sub(r'#+\s*\d*\.?\s*', '', linha) # Remove Headers e números de tópicos
        linha = re.sub(r'\*\*', '', linha)  # Remove Negrito
        linha = re.sub(r'\*', '', linha)    # Remove Itálico
        linha = re.sub(r'`', '', linha)     # Remove Inline Code
        linha = re.sub(r'^-\s+', '', linha) # Remove bullets (hífen no início)
        
        # Humanizar leituras específicas (dois pontos viram pausa verbal)
        linha = linha.replace(":", ",")
        
        # Ajustes de pronúncia técnica
        linha = linha.replace("ERC-20", "E R C 20")
        linha = linha.replace("ERC-721", "E R C 721")
        linha = linha.replace("EIP-2612", "E I P 26 12")
        linha = linha.replace("v5.0", "versão 5.0")
        linha = linha.replace("dApp", "Aplicação Descentralizada")
        linha = linha.replace("Sepolia", "Sepólia")
        linha = linha.replace("EVM", "E V M")
        linha = linha.replace("DAO", "Dá o")
        linha = linha.replace("nonReentrant", "Non Re Entrant")
        linha = linha.replace("onlyOwner", "Only Owner")
        linha = linha.replace("ETH/USD", "Etherium para Dólar")
        linha = linha.replace("AggregatorV3Interface", "Aggregator V3 Interface")
        
        # Se após a limpeza ainda tiver texto
        if len(linha) > 2:
            # Substituir virgula no fim por ponto para fechar a frase
            if linha.endswith(","):
                linha = linha[:-1] + "."
                
            falar(linha)
            time.sleep(0.5) # Pausa humanizada entre linhas para não atropelar a fala
            
    falar("Esta foi a leitura oficial do relatório técnico. Estou à disposição para iniciar os testes práticos.")
    return "Apresentação do relatório técnico concluída."
