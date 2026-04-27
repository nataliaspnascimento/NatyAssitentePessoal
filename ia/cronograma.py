import datetime
import random

# Mapeamento de 'O que mais cai' (Top Incidência)
EDITAIS = {
    "Natalia": {
        "Cargos": ["Auditor SEFAZ-CE", "TJ-CE", "INSS", "ALECE"],
        "Ciclo": [
            {"materia": "Direito Previdenciário", "assunto": "Benefícios em Espécie", "foco": "INSS (70% da prova)"},
            {"materia": "Legislação Tributária", "assunto": "ICMS - Lei Kandir", "foco": "SEFAZ-CE (Peso 3)"},
            {"materia": "Direito Administrativo", "assunto": "Licitações (Lei 14.133)", "foco": "TJ-CE e ALECE"},
            {"materia": "Contabilidade Geral", "assunto": "Balanço Patrimonial", "foco": "SEFAZ e Receita"},
            {"materia": "Direito Constitucional", "assunto": "Artigo 5º e Organização do Estado", "foco": "Todos"},
            {"materia": "Regimento Interno", "assunto": "Processo Legislativo", "foco": "ALECE"},
        ]
    },
    "Hobson": {
        "Cargos": ["TI SEFAZ", "TI TJ-CE", "TI SEFIN", "Polícia Federal TI"],
        "Ciclo": [
            {"materia": "Segurança da Informação", "assunto": "Criptografia e Malwares", "foco": "PF e SEFAZ"},
            {"materia": "Banco de Dados", "assunto": "SQL e Modelagem Relacional", "foco": "SEFIN e TJ-CE"},
            {"materia": "Engenharia de Software", "assunto": "Metodologias Ágeis (SCRUM)", "foco": "Ministério da Fazenda"},
            {"materia": "Redes de Computadores", "assunto": "Modelo OSI e TCP/IP", "foco": "PF e Tribunais"},
            {"materia": "Programação", "assunto": "Linguagem Python e Estrutura de Dados", "foco": "PF (Matéria Ouro)"},
            {"materia": "Governança de TI", "assunto": "COBIT e ITIL", "foco": "SEFAZ e SEFIN"},
        ]
    }
}

def obter_sugestao_estudo(nome_usuario):
    # Se não for Natalia ou Hobson, assume perfil geral
    perfil = EDITAIS.get(nome_usuario)
    if not perfil:
        return None

    # Seleciona um item do ciclo (pode ser sequencial ou aleatório, aqui faremos aleatório para dinamismo)
    estudo = random.choice(perfil["Ciclo"])
    
    hora = int(datetime.datetime.now().strftime("%H"))
    if 5 <= hora < 12: saudacao = "o dia está maravilhoso"
    elif 12 <= hora < 18: saudacao = "a tarde está produtiva"
    else: saudacao = "a noite está tranquila"

    msg = f"Olá, {'Senhor ' if nome_usuario == 'Hobson' else ''}{nome_usuario}. "
    msg += f"São {datetime.datetime.now().strftime('%H:%M')}, {saudacao} para aprender mais. "
    msg += f"Hoje o nosso foco para os cargos de {', '.join(perfil['Cargos'][:2])} será {estudo['materia']}. "
    msg += f"O assunto principal é {estudo['assunto']}, que tem alta incidência no {estudo['foco']}. "
    msg += "Vamos começar?"
    
    return msg
