"""
Módulo de Perfil de Voz da Naty
Aprende e reconhece vozes com base na frequência vocal.
"""
import json
import os

ARQUIVO_PERFIS = os.path.join(os.path.dirname(__file__), "..", "perfis_voz.json")
TOLERANCIA_HZ  = 50   # Margem de erro aceitável em Hz
MAX_AMOSTRAS   = 30   # Máximo de amostras por pessoa (descarta as mais antigas)


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


def registrar(nome, frequencia):
    """
    Adiciona uma nova amostra de frequência ao perfil de um usuário.
    Se o usuário não existir, cria um novo perfil.
    Retorna a nova média calculada.
    """
    if frequencia <= 0:
        return 0.0

    perfis = _carregar()

    if nome not in perfis:
        perfis[nome] = {"amostras": [], "media": 0.0}
        print(f"[VOZ] Novo usuário registrado: {nome}")
    else:
        print(f"[VOZ] Atualizando perfil de: {nome}")

    # Adiciona amostra e limita ao máximo
    perfis[nome]["amostras"].append(round(frequencia, 2))
    perfis[nome]["amostras"] = perfis[nome]["amostras"][-MAX_AMOSTRAS:]

    # Recalcula média ignorando zeros
    validas = [f for f in perfis[nome]["amostras"] if f > 0]
    media = round(sum(validas) / len(validas), 2) if validas else 0.0
    perfis[nome]["media"]   = media
    perfis[nome]["total"]   = len(validas)

    _salvar(perfis)

    print(f"[VOZ] Perfil '{nome}': {len(validas)} amostras | média={media:.1f}Hz")
    return media


def identificar(frequencia):
    """
    Tenta identificar quem está falando com base na frequência.
    Retorna o nome se encontrar correspondência, None caso contrário.
    """
    if frequencia <= 0:
        return None

    perfis = _carregar()
    if not perfis:
        return None

    melhor_nome = None
    menor_diff  = float("inf")

    for nome, dados in perfis.items():
        media = dados.get("media", 0.0)
        if media <= 0:
            continue
        diff = abs(frequencia - media)
        if diff < menor_diff:
            menor_diff = diff
            melhor_nome = nome

    if melhor_nome and menor_diff <= TOLERANCIA_HZ:
        print(f"[VOZ] Identificado: {melhor_nome} (diff={menor_diff:.1f}Hz)")
        return melhor_nome

    print(f"[VOZ] Voz desconhecida (freq={frequencia:.1f}Hz, menor diff={menor_diff:.1f}Hz)")
    return None


def listar_usuarios():
    """Retorna lista de usuários cadastrados."""
    return list(_carregar().keys())


def resumo():
    """Exibe um resumo dos perfis cadastrados."""
    perfis = _carregar()
    if not perfis:
        print("[VOZ] Nenhum perfil cadastrado.")
        return
    print(f"[VOZ] Perfis cadastrados ({len(perfis)}):")
    for nome, dados in perfis.items():
        print(f"  • {nome}: {dados.get('total', 0)} amostras | média={dados.get('media', 0):.1f}Hz")
