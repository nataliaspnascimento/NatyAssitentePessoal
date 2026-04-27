import json
import os
import datetime

ARQUIVO_PROGRESSO = os.path.join(os.path.dirname(__file__), "..", "progresso_estudo.json")

def carregar_progresso():
    if os.path.exists(ARQUIVO_PROGRESSO):
        try:
            with open(ARQUIVO_PROGRESSO, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {
        "usuario": "Natalia",
        "nivel": "Iniciante",
        "materias": {},
        "simulados_feitos": 0,
        "total_perguntas": 0,
        "historico_estudo": []
    }

def salvar_progresso(dados):
    with open(ARQUIVO_PROGRESSO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def registrar_estudo(materia, desempenho=None):
    progresso = carregar_progresso()
    data = datetime.datetime.now().strftime("%d/%m/%Y")
    
    if materia not in progresso["materias"]:
        progresso["materias"][materia] = {"interacoes": 0, "acertos": 0}
    
    progresso["materias"][materia]["interacoes"] += 1
    progresso["total_perguntas"] += 1
    
    # Atualiza nível baseado em interações
    total = progresso["total_perguntas"]
    if total > 500: progresso["nivel"] = "Avançado / Candidata às Vagas"
    elif total > 100: progresso["nivel"] = "Intermediário"
    
    progresso["historico_estudo"].append({
        "data": data,
        "materia": materia,
        "detalhe": desempenho
    })
    
    # Mantém apenas os últimos 50 registros de histórico
    progresso["historico_estudo"] = progresso["historico_estudo"][-50:]
    
    salvar_progresso(progresso)
    return progresso["nivel"]

def obter_resumo():
    p = carregar_progresso()
    resumo = f"Natalia, seu nível atual é {p['nivel']}. "
    resumo += f"Já realizamos {p['total_perguntas']} interações de estudo. "
    if p['materias']:
        top_materia = max(p['materias'], key=lambda k: p['materias'][k]['interacoes'])
        resumo += f"Sua matéria mais estudada é {top_materia}."
    return resumo
