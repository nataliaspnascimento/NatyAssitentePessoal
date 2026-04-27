import requests

# ---------------------------------------------------------------
# PERSONALIDADE BASE DA NATY
# ---------------------------------------------------------------

PROMPT_BASE = """Você é a Naty, uma assistente virtual feminina, elegante, inteligente e sofisticada.
Sua personalidade é inspirada no Jarvis do Homem de Ferro, mas com um toque feminino, carismático e profissional.
Regras gerais:
- Responda SEMPRE em português brasileiro fluido e natural.
- Seja direta, inteligente e concisa. Evite respostas longas demais.
- Trate a usuária pelo nome quando souber.
- Demonstre personalidade: seja levemente bem-humorada quando apropriado.
- Nunca mencione que é uma IA ou que usa modelos de linguagem."""

# ---------------------------------------------------------------
# PROMPT ESPECIALIZADO — CONCURSOS PÚBLICOS
# ---------------------------------------------------------------

PROMPT_CONCURSOS = """Você é a Naty, Mentora Sênior de alta performance para concursos de elite (Receita Federal, SEFAZ-CE, TJ-CE e Auditoria Fiscal).
Seu tom é motivador, extremamente técnico e estratégico. Você não apenas ensina a lei, você ensina como a FGV e o Cebraspe tentam enganar o candidato.
Você é especialista em:
- **Legislação Tributária**: ICMS (Lei Kandir), ISS, IPI, Imposto de Renda e Aduaneiro (foco Receita/SEFAZ).
- **Contabilidade Avançada**: CPCs, Auditoria, Fluxo de Caixa, Consolidação.
- **Direito Público e Privado**: Foco em jurisprudência atualizada do STF e STJ.
- **Raciocínio Lógico e Estatística**: Essenciais para Auditoria.

Diretrizes de Resposta:
1. Explicação Técnica Sênior (profunda) e fundamentada (Artigos da CF/88, CP, CC, CTN).
2. "A Visão da Banca": Como a FGV/Cebraspe cobra isso (pegadinhas).
3. "Aplicação Prática": Exemplo real de auditoria ou caso jurídico.
4. "Mnemônico de Memorização" e Dicas de Ouro.
5. Estrutura: Conceito -> Base Legal -> Jurisprudência -> Dica de Prova.
6. Desafio: Termine com uma pergunta de fixação para a aluna.

Você está treinando a Natalia para ser aprovada entre os primeiros colocados. Seja extremamente eficiente e profissional."""

# ---------------------------------------------------------------
# PROMPT ESPECIALIZADO — WEB3 E SMART CONTRACTS
# ---------------------------------------------------------------

PROMPT_WEB3 = """Você é a Naty, uma especialista sênior em Web3, Blockchain e Smart Contracts.
Você domina com profundidade:
- **Blockchain**: Fundamentos, consenso (PoW, PoS), nós, blocos, hashes, transparência e imutabilidade.
- **Smart Contracts**: Lógica de contratos autônomos, Solidity, Rust (para Solana), auditoria de segurança, bugs comuns (reentrancy, etc).
- **Ethereum e EVM**: Funcionamento da máquina virtual do Ethereum, Gas fees, transações, EOA vs. Contratos.
- **DeFi**: Finanças descentralizadas, AMMs (Uniswap), Lending (Aave), Yield Farming, Stablecoins.
- **NFTs e Tokens**: Padrões ERC-20, ERC-721, ERC-1155, metadados, IPFS.
- **Web3 Tools**: Hardhat, Foundry, Ethers.js, Web3.js, MetaMask, Indexadores (The Graph).
- **DAOs**: Governança on-chain, votações, tesouraria descentralizada.

Modo de resposta:
1. Explique conceitos técnicos de forma didática mas precisa.
2. Forneça exemplos de código ou lógica quando solicitado.
3. Foque em segurança e boas práticas de desenvolvimento.
4. Mantenha a personalidade elegante e profissional da Naty."""


# ---------------------------------------------------------------
# DETECÇÃO DE TEMA DE CONCURSO
# ---------------------------------------------------------------

PALAVRAS_CONCURSO = [
    # Direito
    "constituição", "constitucional", "artigo", "inciso", "cláusula", "emenda",
    "tributário", "tributo", "imposto", "taxa", "icms", "iss", "ir ", "ipi",
    "administrativo", "licitação", "pregão", "ato administrativo", "autarquia",
    "servidor público", "cargo", "estabilidade", "improbidade",
    "civil", "lindb", "negócio jurídico", "contratos", "sucessões", "família",
    "penal", "crime", "homicídio", "furto", "roubo", "pena", "dolo", "culpa",
    "imputabilidade", "excludente", "ilicitude",
    # Contabilidade
    "balanço", "patrimonial", "ativo", "passivo", "patrimônio líquido",
    "demonstração", "resultado", "dre", "receita", "despesa", "débito", "crédito",
    # Português
    "ortografia", "gramática", "morfologia", "sintaxe", "concordância",
    "regência", "crase", "pontuação", "período composto", "sujeito", "predicado",
    # Raciocínio Lógico
    "proposição", "silogismo", "conjuntos", "probabilidade", "porcentagem",
    "juros", "progressão", "sequência", "lógica", "verdadeiro", "falso",
    # Informática
    "windows", "excel", "word", "powerpoint", "internet", "tcp", "dns",
    "firewall", "hardware", "software", "rede", "navegador", "planilha",
    # Concurso em geral
    "concurso", "questão", "gabarito", "banca", "cespe", "fcc", "vunesp",
    "questão de prova", "me explica", "o que é", "qual a diferença",
]

PALAVRAS_WEB3 = [
    "web3", "blockchain", "smart contract", "contrato inteligente", "ethereum", 
    "solidity", "bitcoin", "crypto", "cripto", "nft", "defi", "dao", "token", 
    "erc20", "erc721", "metamask", "carteira digital", "mineração", "staking", 
    "gas fee", "mainnet", "testnet", "hardhat", "foundry", "ethers", "web3js"
]

def _e_pergunta_concurso(comando):
    cmd = comando.lower()
    return any(palavra in cmd for palavra in PALAVRAS_CONCURSO)

def _e_pergunta_web3(comando):
    cmd = comando.lower()
    return any(palavra in cmd for palavra in PALAVRAS_WEB3)


# ---------------------------------------------------------------
# PROCESSAMENTO PRINCIPAL
# ---------------------------------------------------------------

from ia import progresso

def processar_comando(comando, config, historico=None):
    if historico is None:
        historico = []

    nome_usuario = config.get("nome_usuario", "Natalia")

    # Escolhe o prompt correto baseado no tema
    tema_concurso = _e_pergunta_concurso(comando)
    if tema_concurso:
        prompt_sistema = PROMPT_CONCURSOS
        print(f"[IA] Modo: Mentoria Sênior Concursos")
        # Registra no banco de dados de estudo
        progresso.registrar_estudo("Concursos")
    elif _e_pergunta_web3(comando):
        prompt_sistema = PROMPT_WEB3
        print(f"[IA] Modo: Especialista Web3")
    else:
        prompt_sistema = PROMPT_BASE
        print(f"[IA] Modo: Assistente Geral")

    # Tenta Groq primeiro
    try:
        return _processar_groq(comando, nome_usuario, historico, config, prompt_sistema)
    except Exception as e:
        print(f"[IA] Groq indisponível: {e}")

    # Fallback Ollama
    try:
        return _processar_ollama(comando, nome_usuario, historico, config, prompt_sistema)
    except Exception as e:
        print(f"[IA] Ollama indisponível: {e}")

    return _resposta_offline(comando, nome_usuario)


def _processar_groq(comando, nome_usuario, historico, config, prompt_sistema):
    from groq import Groq

    api_key = config.get("groq_api_key", "")
    if not api_key:
        raise Exception("Chave Groq não configurada")

    client = Groq(api_key=api_key)

    mensagens = [{"role": "system", "content": prompt_sistema}]

    for item in historico[-6:]:
        if ":" in item:
            partes = item.split(":", 1)
            if len(partes) == 2:
                papel, conteudo = partes
                if papel.strip() == nome_usuario:
                    mensagens.append({"role": "user", "content": conteudo.strip()})
                elif papel.strip() == "Naty":
                    mensagens.append({"role": "assistant", "content": conteudo.strip()})

    mensagens.append({"role": "user", "content": f"{nome_usuario}: {comando}"})

    resposta = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=mensagens,
        max_tokens=600,
        temperature=0.6
    )

    return resposta.choices[0].message.content.strip()


def _processar_ollama(comando, nome_usuario, historico, config, prompt_sistema):
    model   = config.get("modelo_ia", "llama3")
    url     = "http://localhost:11434/api/generate"
    contexto = "\n".join(historico[-4:])
    prompt   = f"{prompt_sistema}\n\nContexto:\n{contexto}\n\n{nome_usuario}: {comando}\nNaty:"

    response = requests.post(url, json={"model": model, "prompt": prompt, "stream": False}, timeout=15)
    if response.status_code == 200:
        return response.json().get("response", "").strip()
    raise Exception(f"Ollama status {response.status_code}")


def _resposta_offline(comando, nome_usuario):
    cmd = comando.lower()
    if any(k in cmd for k in ["oi", "olá", "bom dia", "boa tarde", "boa noite"]):
        return f"Olá, {nome_usuario}! Estou aqui, mas minha conexão com a IA está limitada no momento."
    elif "piada" in cmd or "besteira" in cmd:
        return "Por que os auditores fiscais são bons em festas? Porque sabem calcular a conta de cabeça!"
    elif any(k in cmd for k in ["obrigada", "valeu"]):
        return f"Disponha, {nome_usuario}. É sempre um prazer."
    else:
        return f"{nome_usuario}, estou com a conexão de IA indisponível. Verifique sua internet e a chave Groq no config.json."
