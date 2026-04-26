import subprocess
import socket
import urllib.parse

def pesquisar_web(termo):
    """Abre o navegador padrão com a pesquisa no Google."""
    if not termo or len(termo.strip()) < 2:
        return "O que você gostaria que eu pesquisasse?"
    termo_codificado = urllib.parse.quote(termo.strip())
    url = f"https://www.google.com/search?q={termo_codificado}"
    try:
        subprocess.Popen(f'start "" "{url}"', shell=True)
        return f"Pesquisando por '{termo}' no Google."
    except:
        return f"Não consegui abrir o navegador para pesquisar."

def abrir_url(url):
    """Abre uma URL diretamente no navegador."""
    if not url.startswith("http"):
        url = "https://" + url
    try:
        subprocess.Popen(f'start "" "{url}"', shell=True)
        return f"Abrindo {url}."
    except:
        return "Não consegui abrir o link."

def obter_ip_local():
    """Retorna o IP local da máquina."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return f"Seu endereço IP local é {ip}."
    except:
        return "Não consegui determinar seu endereço IP."

def verificar_conexao():
    """Verifica se há conexão com a internet."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return "Sua conexão com a internet está ativa."
    except OSError:
        return "Parece que você está sem internet no momento."
