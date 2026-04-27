"""
Módulo de Biometria Vocal Avançada da Naty.
Utiliza múltiplas amostras para criar uma assinatura digital de voz.
"""
import json
import os
import numpy as np

ARQUIVO_PERFIS = os.path.join(os.path.dirname(__file__), "..", "perfis_voz.json")
TOLERANCIA_PADRAO = 80  # Hz de diferença máxima (mais tolerante para zero-crossing)
MIN_AMOSTRAS_TREINO = 1  # Treino imediato na primeira vez

def _carregar():
    if os.path.exists(ARQUIVO_PERFIS):
        try:
            with open(ARQUIVO_PERFIS, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}

def _salvar(perfis):
    with open(ARQUIVO_PERFIS, "w", encoding="utf-8") as f:
        json.dump(perfis, f, indent=4, ensure_ascii=False)

def registrar_amostra(nome, frequencia):
    """Adiciona uma amostra ao treinamento do usuário."""
    if frequencia <= 50: return False # Ignora ruído baixo
    
    # Validação: Ignora nomes que parecem ser frases completas (mais de 3 palavras)
    if not nome or len(nome.split()) > 3:
        print(f"[PERFIL] Nome ignorado por ser muito longo ou inválido: {nome}")
        return False
    
    perfis = _carregar()
    if nome not in perfis:
        perfis[nome] = {"amostras": [], "media": 0.0, "treinado": False}
    
    perfis[nome]["amostras"].append(round(frequencia, 2))
    
    # Recalcula média
    validas = perfis[nome]["amostras"]
    perfis[nome]["media"] = round(sum(validas) / len(validas), 2)
    
    # Verifica se completou o treinamento básico
    if len(validas) >= MIN_AMOSTRAS_TREINO:
        perfis[nome]["treinado"] = True
        
    _salvar(perfis)
    return perfis[nome]["treinado"]

def identificar(frequencia):
    """
    Identifica o usuário com base na assinatura vocal.
    Retorna (nome, treinado) ou (None, False).
    """
    if frequencia <= 50: return None, False
    
    perfis = _carregar()
    melhor_match = None
    menor_diff = float('inf')
    
    for nome, dados in perfis.items():
        media = dados.get("media", 0)
        diff = abs(frequencia - media)
        
        if diff < menor_diff and diff <= TOLERANCIA_PADRAO:
            menor_diff = diff
            melhor_match = nome
            
    if melhor_match:
        return melhor_match, perfis[melhor_match].get("treinado", False)
    return None, False

def renomear_usuario(nome_antigo, nome_novo):
    """
    Renomeia um perfil de voz ou mescla com um existente.
    Útil para correções de nome em tempo real.
    """
    if not nome_antigo or not nome_novo: return False
    
    perfis = _carregar()
    if nome_antigo not in perfis:
        return False
    
    dados_antigos = perfis.pop(nome_antigo)
    
    if nome_novo in perfis:
        # Mescla as amostras
        perfis[nome_novo]["amostras"].extend(dados_antigos["amostras"])
        perfis[nome_novo]["amostras"] = perfis[nome_novo]["amostras"][-20:] # Limita histórico
        
        # Recalcula média
        validas = perfis[nome_novo]["amostras"]
        perfis[nome_novo]["media"] = round(sum(validas) / len(validas), 2)
        perfis[nome_novo]["treinado"] = len(validas) >= MIN_AMOSTRAS_TREINO
    else:
        # Apenas cria a nova chave
        perfis[nome_novo] = dados_antigos
        
    _salvar(perfis)
    print(f"[PERFIL] Nome corrigido de '{nome_antigo}' para '{nome_novo}'.")
    return True

def limpar_banco():
    """Zera todos os perfis para re-treinamento."""
    if os.path.exists(ARQUIVO_PERFIS):
        os.remove(ARQUIVO_PERFIS)
    return True
