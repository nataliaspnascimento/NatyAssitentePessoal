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
from comandos import sistema, arquivos
from comandos import apps, rede, utilidades
from voz import perfil as perfil_voz

# Config global (carregada no main)
_config = {}

# -------------------------------------------------------------------
# INICIAR OLLAMA (se encontrado)
# -------------------------------------------------------------------

def tentar_iniciar_ollama():
    caminhos = [
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Ollama", "ollama app.exe"),
        r"C:\Program Files\Ollama\ollama.exe",
        r"C:\Program Files (x86)\Ollama\ollama.exe",
    ]
    for caminho in caminhos:
        if os.path.exists(caminho):
            print(f"[OLLAMA] Encontrado em: {caminho}")
            subprocess.Popen([caminho], close_fds=True)
            time.sleep(5)
            return True
    print("[OLLAMA] Nao encontrado nos caminhos padrao. Inicie manualmente.")
    return False

# -------------------------------------------------------------------
# LOOP PRINCIPAL DA ASSISTENTE
# -------------------------------------------------------------------

NOMES_ACEITOS = ["naty", "nati", "nat", "natali", "natalia"]

def loop_assistente(app):
    historico = []
    usuario_atual = "Natalia"

    while True:
        try:
            app.atualizar_status("Aguardando...")
            resultado = ouvir()

            # ouvir() pode retornar (texto, freq) ou só texto dependendo da versão
            if isinstance(resultado, tuple):
                texto_capturado, frequencia = resultado
            else:
                texto_capturado, frequencia = resultado, 0

            if not texto_capturado:
                continue

            texto = texto_capturado.lower()
            chamou = any(nome in texto for nome in NOMES_ACEITOS)

            if not chamou:
                continue

            # --- Identificação de Usuário com Aprendizado ---
            quem_fala = perfil_voz.identificar(frequencia)

            if quem_fala is None:
                # Voz desconhecida: pede o nome
                falar("Perdão, não reconheço sua voz. Qual é o seu nome?")
                resposta_nome = ouvir()
                if isinstance(resposta_nome, tuple):
                    nome_novo, freq_nome = resposta_nome
                else:
                    nome_novo, freq_nome = resposta_nome, 0

                if nome_novo:
                    # Salva a frequência do chamado inicial (mais representativa)
                    perfil_voz.registrar(nome_novo, frequencia)
                    # Salva também a frequência ao dizer o nome (mais amostras = mais preciso)
                    if freq_nome > 0:
                        perfil_voz.registrar(nome_novo, freq_nome)
                    falar(f"Prazer em conhecê-la, {nome_novo}. Memorizei sua assinatura de voz e vou reconhecê-la nas próximas vezes.")
                    usuario_atual = nome_novo
                else:
                    falar("Não entendi seu nome. Pode me chamar novamente?")
                    continue
            else:
                # Voz reconhecida: reforça o aprendizado com nova amostra
                perfil_voz.registrar(quem_fala, frequencia)
                usuario_atual = quem_fala

            # --- Extrai o comando (remove o nome da assistente) ---
            app.atualizar_status("Processando...")
            comando = texto
            for nome in NOMES_ACEITOS:
                comando = comando.replace(nome, "").strip()

            # Se chamou sem dar comando, pergunta o que quer
            if not comando or len(comando) < 2:
                falar(f"Sim, {usuario_atual}? O que deseja?")
                novo = ouvir()
                comando = (novo[0] if isinstance(novo, tuple) else novo) or ""

            if not comando:
                continue

            app.atualizar_comando(comando)

            # --- Roteamento de Comandos ---
            resposta = ""

            # Despedida
            if any(k in comando for k in ["tchau", "ate logo", "encerrar"]):
                falar(f"Ate logo, {usuario_atual}. Estarei aqui se precisar.")
                os._exit(0)

            # Arquivos
            elif "organiza" in comando:
                resposta = arquivos.organizar_desktop()

            # Volume
            elif "volume" in comando:
                if any(k in comando for k in ["aumenta", "sobe", "mais"]):
                    resposta = sistema.controlar_volume("aumentar")
                elif any(k in comando for k in ["diminui", "abaixa", "menos"]):
                    resposta = sistema.controlar_volume("diminuir")
                else:
                    resposta = sistema.controlar_volume("mudo")

            # Saude do PC
            elif any(k in comando for k in ["ram", "cpu", "memoria", "computador"]):
                resposta = sistema.obter_saude_pc()

            # Desligar
            elif "desligar" in comando:
                minutos = re.findall(r'\d+', comando)
                tempo = int(minutos[0]) if minutos else 0
                resposta = sistema.gerenciar_energia("desligar", tempo)

            elif "cancelar" in comando and "desligamento" in comando:
                resposta = sistema.gerenciar_energia("cancelar")

            # Lembrete
            elif "lembre" in comando:
                from comandos import lembretes
                if "de " in comando and "daqui a " in comando:
                    tarefa = comando.split("de ")[1].split("daqui a ")[0].strip()
                    tempo_txt = comando.split("daqui a ")[1].strip()
                    resposta = lembretes.agendar_lembrete(tarefa, tempo_txt, falar)
                else:
                    resposta = "Para agendar, diga: 'me lembre de tomar agua daqui a 10 minutos'."

            # ── APPS ───────────────────────────────────────────
            elif any(k in comando for k in ["abre ", "abrir ", "inicia ", "iniciar ", "lança "]):
                # Extrai o nome do programa
                for gatilho in ["abre ", "abrir ", "inicia ", "iniciar ", "lança "]:
                    if gatilho in comando:
                        nome_app = comando.split(gatilho, 1)[1].strip()
                        break
                resposta = apps.abrir_programa(nome_app)

            elif any(k in comando for k in ["fecha ", "fechar ", "encerra "]):
                for gatilho in ["fecha ", "fechar ", "encerra "]:
                    if gatilho in comando:
                        nome_app = comando.split(gatilho, 1)[1].strip()
                        break
                resposta = apps.fechar_programa(nome_app)

            # ── PESQUISA WEB ────────────────────────────────────
            elif any(k in comando for k in ["pesquisa ", "pesquisar ", "busca ", "buscar ", "google "]):
                for gatilho in ["pesquisa ", "pesquisar ", "busca ", "buscar ", "google "]:
                    if gatilho in comando:
                        termo = comando.split(gatilho, 1)[1].strip()
                        break
                resposta = rede.pesquisar_web(termo)

            elif "abre o site" in comando or "abre o link" in comando or "abrir site" in comando:
                partes = comando.replace("abre o site", "").replace("abre o link", "").replace("abrir site", "").strip()
                resposta = rede.abrir_url(partes)

            elif "meu ip" in comando or "endereço ip" in comando:
                resposta = rede.obter_ip_local()

            elif "internet" in comando or "conexão" in comando or "conectado" in comando:
                resposta = rede.verificar_conexao()

            # ── SCREENSHOT ─────────────────────────────────────
            elif any(k in comando for k in ["print", "screenshot", "captura de tela", "tira um print"]):
                resposta = utilidades.tirar_screenshot()

            # ── NOTAS ──────────────────────────────────────────
            elif "cria uma nota" in comando or "criar nota" in comando or "salva uma nota" in comando:
                # Extrai o conteúdo após 'nota:' ou 'nota '
                conteudo = ""
                for sep in ["nota:", "nota "]:
                    if sep in comando:
                        conteudo = comando.split(sep, 1)[1].strip()
                        break
                if conteudo:
                    resposta = utilidades.criar_nota(conteudo)
                else:
                    falar("O que devo anotar?")
                    novo_cmd = ouvir()
                    conteudo = (novo_cmd[0] if isinstance(novo_cmd, tuple) else novo_cmd) or ""
                    resposta = utilidades.criar_nota(conteudo) if conteudo else "Não entendi o que anotar."

            elif "lista minhas notas" in comando or "minhas notas" in comando:
                resposta = utilidades.listar_notas()

            elif "abre minha pasta" in comando or "pasta da naty" in comando:
                resposta = utilidades.abrir_pasta_naty()

            # ── HORAS / DATA ────────────────────────────────────
            elif any(k in comando for k in ["horas", "que horas"]):
                resposta = time.strftime("Agora sao %H horas e %M minutos.")
            elif any(k in comando for k in ["data", "dia"]):
                resposta = time.strftime("Hoje e dia %d de %m de %Y.")

            # Fallback para IA (Groq / Ollama)
            else:
                config = dict(_config)  # Usa config global com chave Groq
                config["nome_usuario"] = usuario_atual
                resposta = processar_comando(comando, config, historico)

            # Atualiza histórico e fala
            historico.append(f"{usuario_atual}: {comando}")
            historico.append(f"Naty: {resposta}")
            if len(historico) > 10:
                historico = historico[-10:]

            app.atualizar_status("Respondendo...")
            falar(resposta)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"[ERRO NO LOOP] {e}")
            time.sleep(1)

# -------------------------------------------------------------------
# INICIALIZAÇÃO
# -------------------------------------------------------------------

def carregar_config():
    """Carrega as configurações do arquivo config.json."""
    caminho = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[CONFIG] Erro ao carregar config.json: {e}")
        return {}

def main():
    global _config
    _config = carregar_config()
    print(f"[CONFIG] Chave Groq: {'configurada ✓' if _config.get('groq_api_key') else 'NÃO configurada ✗'}")

    threading.Thread(target=tentar_iniciar_ollama, daemon=True).start()

    root = tk.Tk()
    app_interface = JanelaNaty(root)

    thread_ia = threading.Thread(target=loop_assistente, args=(app_interface,), daemon=True)
    thread_ia.start()

    def saudacao():
        time.sleep(3)
        falar("Sistemas online. Natalia, estou pronta para servir.")

    threading.Thread(target=saudacao, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    main()
