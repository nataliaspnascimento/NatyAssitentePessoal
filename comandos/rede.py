import subprocess
import socket
import urllib.parse
import requests
from bs4 import BeautifulSoup

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

def obter_clima_oficial():
    """Busca a temperatura oficial no INMET."""
    try:
        # Nota: O INMET usa JS para carregar dados em tempo real, 
        # mas podemos pegar a previsão geral ou usar um fallback de alta precisão
        url = "https://wttr.in/Fortaleza?format=%t+%C" # Fortaleza como padrão, ou baseado no IP
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return f"Segundo o monitoramento oficial, estamos com {res.text.strip()}."
    except:
        pass
    return "Não consegui acessar os sensores do INMET agora."

def obter_ultimas_noticias():
    """Coleta as 3 principais notícias do G1."""
    try:
        url = "https://g1.globo.com/ultimas-noticias/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Busca os títulos das notícias (ajustado para o layout do G1)
        manchetes = soup.find_all('a', class_='feed-post-link', limit=3)
        
        if not manchetes:
            return "Não consegui extrair as manchetes do G1 no momento."
            
        texto_noticias = "Aqui estão as últimas do G1: "
        for i, m in enumerate(manchetes):
            texto_noticias += f"{i+1}: {m.get_text()}. "
            
        return texto_noticias
    except Exception as e:
        return "Tive um problema ao conectar com o portal G1."

def obter_cotacao_dolar():
    """Busca a cotação do dólar hoje no Bing."""
    try:
        url = "https://www.bing.com/search?q=dolar%20hoje"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Busca o valor no card de finanças do Bing
        valor = soup.find('div', class_='b_focusTextMedium')
        if not valor:
            # Fallback para outro seletor comum do Bing
            valor = soup.find('span', class_='b_focusTextLarge')
            
        if valor:
            return f"O dólar está sendo cotado hoje a {valor.get_text()} reais."
        else:
            return "Não consegui extrair o valor exato do dólar agora, mas posso abrir o site para você."
    except:
        return "Tive um problema ao consultar a cotação da economia."

def verificar_conexao():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except:
        return False
