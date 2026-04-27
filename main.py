import tkinter as tk
import threading
import time
import os
import json
import re
import subprocess

from interface.janela import JanelaNaty
from voz.ouvir import ouvir
from voz.falar import falar
from ia.cerebro import processar_comando
from comandos import sistema, arquivos, apps, rede, utilidades
from voz import perfil as perfil_voz
from ia import cronograma, progresso

# Config global
_config = {}

# -------------------------------------------------------------------
# INICIAR OLLAMA (se encontrado)
# -------------------------------------------------------------------

def tentar_iniciar_ollama():
    caminhos = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Ollama", "ollama app.exe"),
        r"C:\Program Files\Ollama\ollama.exe"
    ]
    for p in caminhos:
        if os.path.exists(p):
            try:
                subprocess.Popen(p, shell=True)
                print(f"[OLLAMA] Iniciado automaticamente em {p}")
                return True
            except:
                pass
    print("[OLLAMA] Não encontrado. Inicie manualmente se quiser usar IA local.")
    return False

# -------------------------------------------------------------------
# LOOP PRINCIPAL DA ASSISTENTE
# -------------------------------------------------------------------

NOMES_ACEITOS = ["naty", "nati", "nat", "natali", "natalia"]

def loop_assistente(app):
    historico = []

    while True:
        try:
            # Aguarda a saudação inicial terminar para não "ouvir a si mesma"
            if not app.inicializado:
                time.sleep(0.5)
                continue

            app.atualizar_status("Aguardando...")
            resultado = ouvir()

            if isinstance(resultado, tuple):
                texto_capturado, frequencia = resultado
            else:
                texto_capturado, frequencia = resultado, 0

            if not texto_capturado or len(texto_capturado.strip()) < 2:
                continue

            texto = texto_capturado.lower()
            
            # --- Lógica de Correção de Nome (Tempo Real) ---
            if any(k in texto for k in ["meu nome não é", "não sou o", "não sou a", "corrija meu nome"]):
                # Padrão: "me chamo X" ou "meu nome é X" ou "sou o X"
                match = re.search(r"(?:me chamo|meu nome é|sou o|sou a|sou|meu nome)\s+([a-zà-ú\s]+)", texto, re.IGNORECASE)
                if match:
                    novo_nome = match.group(1).strip().title()
                    nome_antigo = usuario_atual
                    
                    # Atualiza biometria e sessão
                    perfil_voz.renomear_usuario(nome_antigo, novo_nome)
                    usuario_atual = novo_nome
                    
                    msg_confirmacao = f"Peço desculpas, {novo_nome}! Já corrigi seu nome no meu banco de dados. Como posso ajudar agora?"
                    app.atualizar_status("Respondendo...")
                    falar(msg_confirmacao)
                    continue
            
            # --- Lógica de Ativação ---
            # Ela responde se: 
            # 1. Você chamar pelo nome
            # 2. Ela acabou de perguntar algo e está esperando resposta
            chamou = any(nome in texto for nome in NOMES_ACEITOS)
            
            # Se não chamou o nome, ela só processa se o histórico estiver "quente" (conversa em andamento)
            # Mas para garantir eficácia total como você pediu, vamos deixar ela processar TUDO o que ouvir
            # de forma inteligente.
            
            app.atualizar_status("Processando...")
            comando = texto
            for nome in NOMES_ACEITOS:
                comando = comando.replace(nome, "").strip()

            # --- Identificação de Usuário Inteligente ---
            quem_fala, esta_treinado = perfil_voz.identificar(frequencia)

            if quem_fala:
                app.usuario_atual = quem_fala
                perfil_voz.registrar_amostra(quem_fala, frequencia)
            # Se não identificou pela voz, mas já temos um nome na sessão, usamos ele
            # e registramos a nova amostra para aprender essa voz nova.
            elif app.usuario_atual and app.usuario_atual != "Visitante":
                perfil_voz.registrar_amostra(app.usuario_atual, frequencia)
            
            usuario_atual = app.usuario_atual
            resposta = None

            # ── SISTEMA / HARDWARE ────────────────────────────
            if "volume" in comando:
                if any(k in comando for k in ["aumenta", "sobe", "mais"]):
                    resposta = sistema.controlar_volume("aumentar")
                elif any(k in comando for k in ["diminui", "abaixa", "menos"]):
                    resposta = sistema.controlar_volume("diminuir")
                else:
                    resposta = sistema.controlar_volume("mudo")

            elif any(re.search(fr"\b{k}\b", comando) for k in ["ram", "cpu", "memória", "memoria", "computador"]):
                resposta = sistema.obter_saude_pc()

            elif "desligar" in comando:
                minutos = re.findall(r'\d+', comando)
                tempo = int(minutos[0]) if minutos else 0
                resposta = sistema.gerenciar_energia("desligar", tempo)

            # ── APPS ───────────────────────────────────────────
            elif any(k in comando for k in ["abre ", "abrir ", "inicia ", "iniciar "]):
                nome_app = ""
                for g in ["abre ", "abrir ", "inicia ", "iniciar "]:
                    if g in comando:
                        nome_app = comando.split(g, 1)[1].strip()
                        break
                if nome_app: resposta = apps.abrir_programa(nome_app)

            # ── PESQUISA / REDE ────────────────────────────────
            elif any(k in comando for k in ["pesquisa ", "busca "]):
                termo = ""
                for g in ["pesquisa ", "busca "]:
                    if g in comando:
                        termo = comando.split(g, 1)[1].strip()
                        break
                if termo: resposta = rede.pesquisar_web(termo)

            elif any(k in comando for k in ["notícia", "noticias", "acontecendo"]):
                app.atualizar_status("Lendo G1...")
                resposta = rede.obter_ultimas_noticias()

            elif any(k in comando for k in ["dólar", "dolar", "cotação", "economia"]):
                app.atualizar_status("Consultando Bing...")
                resposta = rede.obter_cotacao_dolar()

            # ── UTILIDADES ─────────────────────────────────────
            elif any(k in comando for k in ["print", "screenshot", "captura"]):
                resposta = utilidades.tirar_screenshot()

            elif "nota" in comando and ("cria" in comando or "salva" in comando):
                conteudo = comando.split("nota", 1)[1].strip()
                resposta = utilidades.criar_nota(conteudo) if conteudo else "O que devo anotar?"

            # ── ESTUDOS / CRONOGRAMA ───────────────────────────
            elif "vamos estudar" in comando or "começar estudo" in comando:
                sugestao = cronograma.obter_sugestao_estudo(usuario_atual)
                if sugestao:
                    resposta = sugestao
                else:
                    resposta = f"Olá {usuario_atual}, vamos estudar! Qual matéria você deseja revisar hoje?"

            # ── HORAS / DATA ────────────────────────────────────
            elif any(k in comando for k in ["horas", "que horas"]):
                resposta = time.strftime("Agora são %H horas e %M minutos.")

            # ── INTELIGÊNCIA ARTIFICIAL (CONCURSOS / WEB3 / GERAL) ──
            # Se não caiu em nenhum comando de sistema, vai para a IA
            if not resposta:
                config_ia = dict(_config)
                config_ia["nome_usuario"] = usuario_atual
                
                app.atualizar_status("Processando...")
                resposta = processar_comando(comando, config_ia, historico)

            # --- Finalização e Fala Obrigatória ---
            if not resposta:
                resposta = "Desculpe, Natalia, eu processei sua solicitação mas não consegui gerar uma resposta verbal. Pode repetir?"

            # Atualiza histórico (limita a 10 itens)
            historico.append(f"{usuario_atual}: {comando}")
            historico.append(f"Naty: {resposta}")
            historico = historico[-10:]

            # Ação de falar é obrigatória aqui
            app.atualizar_status("Respondendo...")
            app.atualizar_comando(comando)
            falar(resposta)

        except Exception as e:
            msg_erro = f"Ocorreu um erro no meu sistema de processamento. {str(e)}"
            print(f"[ERRO NO LOOP] {e}")
            falar(msg_erro)
            time.sleep(1)

# -------------------------------------------------------------------
# INICIALIZAÇÃO
# -------------------------------------------------------------------

def carregar_config():
    caminho = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        if os.path.exists(caminho):
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return {}

def main():
    global _config
    _config = carregar_config()
    
    # Inicia Ollama em background se houver
    threading.Thread(target=tentar_iniciar_ollama, daemon=True).start()

    root = tk.Tk()
    app = JanelaNaty(root)

    # Inicia o loop da assistente em uma thread separada
    threading.Thread(target=loop_assistente, args=(app,), daemon=True).start()

    # --- Sequência de Saudação Premium ---
    def sequencia_inicial():
        time.sleep(2)
        
        # 1. Apresentação Inicial
        app.atualizar_status("Respondendo...")
        falar("Olá! Meu nome é Naty, sou a assistente Pessoal da Natalia. Com quem falo?")
        app.atualizar_status("Aguardando...")
        
        # 2. Ouve e Identifica
        captura = ouvir()
        nome_falado = ""
        frequencia = 0
        
        if isinstance(captura, tuple):
            texto_bruto, frequencia = captura
            # Extração inteligente: "Meu nome é Robson" -> "Robson"
            if texto_bruto:
                match = re.search(r"(?:meu nome é|me chamo|sou o|sou a|pode me chamar de)\s+([a-zà-ú\s]+)", texto_bruto, re.IGNORECASE)
                if match:
                    nome_falado = match.group(1).strip().title()
                else:
                    nome_falado = texto_bruto.strip().title()
            else:
                nome_falado = "Visitante"
        else:
            nome_falado = str(captura or "Visitante").strip().title()

        # Tenta identificar pela voz, mas prioriza o nome que ele ACABOU de dizer
        quem_e, _ = perfil_voz.identificar(frequencia)
        
        # Se ele disse um nome válido, usamos o que ele disse. 
        # Caso contrário, usamos a identificação por voz.
        if nome_falado and nome_falado != "Visitante":
            nome_final = nome_falado
        else:
            nome_final = quem_e if quem_e else "Visitante"

        # REGISTRO IMEDIATO E ATUALIZAÇÃO GLOBAL
        if frequencia > 50 and nome_final != "Visitante":
            # Se a voz era de outro perfil (ex: "Usuário"), renomeamos para o nome novo
            if quem_e and quem_e != nome_final and quem_e != "Visitante":
                perfil_voz.renomear_usuario(quem_e, nome_final)
            else:
                perfil_voz.registrar_amostra(nome_final, frequencia)
            
            app.usuario_atual = nome_final
        
        nome_final = app.usuario_atual

        # 3. Saudação por Horário
        hora = int(time.strftime("%H"))
        if 5 <= hora < 12:   periodo = "Bom dia"
        elif 12 <= hora < 18: periodo = "Boa tarde"
        else:                periodo = "Boa noite"

        # 4. Busca Clima Oficial (INMET via rede)
        clima = rede.obter_clima_oficial()
        
        # 5. Resposta Final Personalizada
        msg = f"{periodo}, {nome_final}! {clima} Em que posso ser útil hoje? Se quiser, posso ler as últimas notícias do G1 para você."
        app.atualizar_status("Respondendo...")
        falar(msg)
        app.atualizar_status("Online")
        
        # 6. Libera o loop principal após a fala terminar
        time.sleep(1) # Pausa de segurança para limpar eco
        app.inicializado = True

    threading.Thread(target=sequencia_inicial, daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()
