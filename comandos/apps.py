import subprocess
import os

# Mapeamento de nomes falados → comandos/caminhos
PROGRAMAS = {
    # Navegadores
    "chrome":       ["chrome", r"C:\Program Files\Google\Chrome\Application\chrome.exe"],
    "firefox":      ["firefox"],
    "edge":         ["msedge"],

    # Desenvolvimento
    "vs code":      ["code"],
    "vscode":       ["code"],
    "terminal":     ["wt"],                        # Windows Terminal
    "powershell":   ["powershell"],
    "cmd":          ["cmd"],
    "git bash":     [r"C:\Program Files\Git\git-bash.exe"],

    # Produtividade
    "word":         ["winword"],
    "excel":        ["excel"],
    "powerpoint":   ["powerpnt"],
    "notepad":      ["notepad"],
    "bloco de notas": ["notepad"],
    "calculadora":  ["calc"],
    "paint":        ["mspaint"],

    # Sistema
    "explorador":   ["explorer"],
    "gerenciador de tarefas": ["taskmgr"],
    "painel de controle":     ["control"],
    "configurações":          ["ms-settings:"],
    "bluetooth":              ["ms-settings:bluetooth"],

    # Mídia
    "spotify":      ["spotify"],
    "discord":      ["discord"],
    "vlc":          [r"C:\Program Files\VideoLAN\VLC\vlc.exe"],
    "obs":          ["obs64"],
}

def abrir_programa(nome_falado):
    """
    Tenta abrir um programa pelo nome falado.
    Procura no dicionário e também tenta diretamente.
    """
    nome = nome_falado.lower().strip()

    # Busca no dicionário
    caminhos = None
    for chave, lista_cmds in PROGRAMAS.items():
        if chave in nome:
            caminhos = lista_cmds
            break

    # Se não achou no dicionário, tenta diretamente
    if not caminhos:
        caminhos = [nome]

    for cmd in caminhos:
        try:
            subprocess.Popen(cmd, shell=True)
            return f"Abrindo {nome_falado.title()} agora, Natalia."
        except FileNotFoundError:
            continue
        except Exception as e:
            continue

    return f"Não encontrei o programa '{nome_falado}'. Verifique se está instalado."

def fechar_programa(nome_falado):
    """Encerra um programa pelo nome do processo."""
    mapa_processos = {
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "edge": "msedge.exe",
        "vs code": "Code.exe",
        "vscode": "Code.exe",
        "word": "WINWORD.EXE",
        "excel": "EXCEL.EXE",
        "spotify": "Spotify.exe",
        "discord": "Discord.exe",
    }
    nome = nome_falado.lower()
    processo = None
    for chave, proc in mapa_processos.items():
        if chave in nome:
            processo = proc
            break

    if not processo:
        processo = nome + ".exe"

    try:
        os.system(f"taskkill /F /IM {processo} 2>NUL")
        return f"Fechei o {nome_falado.title()}."
    except Exception as e:
        return f"Não consegui fechar o {nome_falado}."

def abrir_pasta(caminho=None):
    """Abre uma pasta no Explorer."""
    if not caminho:
        caminho = os.path.expanduser("~")
    try:
        subprocess.Popen(f'explorer "{caminho}"', shell=True)
        return f"Abrindo a pasta no Explorer."
    except:
        return "Não consegui abrir a pasta."
