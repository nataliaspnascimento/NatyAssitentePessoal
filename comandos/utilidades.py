import os
import time
import datetime

# Pasta onde serão salvos prints e notas
PASTA_NATY = os.path.join(os.path.expanduser("~"), "Documents", "Naty")

def _garantir_pasta():
    os.makedirs(PASTA_NATY, exist_ok=True)

# ─────────────────────────────────────────────────────────────
# SCREENSHOT
# ─────────────────────────────────────────────────────────────

def tirar_screenshot(nome_personalizado=None):
    """
    Tira um screenshot da tela e salva na pasta Naty/Documents.
    """
    try:
        import PIL.ImageGrab as ImageGrab
    except ImportError:
        return "Preciso instalar o Pillow. Execute: pip install Pillow"

    _garantir_pasta()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"print_{timestamp}.png" if not nome_personalizado else f"{nome_personalizado}_{timestamp}.png"
    caminho = os.path.join(PASTA_NATY, "Screenshots", nome_arquivo)

    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    try:
        img = ImageGrab.grab()
        img.save(caminho)
        return f"Screenshot salvo como '{nome_arquivo}' na pasta Naty."
    except Exception as e:
        return f"Não consegui tirar o screenshot: {str(e)}"

# ─────────────────────────────────────────────────────────────
# NOTAS DE VOZ
# ─────────────────────────────────────────────────────────────

def criar_nota(texto, titulo=None):
    """
    Cria uma nota de texto salva em arquivo na pasta Naty/Notas.
    """
    _garantir_pasta()

    pasta_notas = os.path.join(PASTA_NATY, "Notas")
    os.makedirs(pasta_notas, exist_ok=True)

    timestamp    = datetime.datetime.now()
    data_legivel = timestamp.strftime("%d/%m/%Y %H:%M")
    nome_arquivo = timestamp.strftime("nota_%Y-%m-%d_%H-%M-%S.txt")

    if not titulo:
        # Usa as primeiras 5 palavras como título
        palavras = texto.strip().split()[:5]
        titulo   = " ".join(palavras).title()

    conteudo = f"{'='*50}\n"
    conteudo += f"📝 {titulo}\n"
    conteudo += f"📅 {data_legivel}\n"
    conteudo += f"{'='*50}\n\n"
    conteudo += texto + "\n"

    caminho = os.path.join(pasta_notas, nome_arquivo)

    try:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return f"Nota '{titulo}' salva com sucesso na pasta Naty."
    except Exception as e:
        return f"Não consegui salvar a nota: {str(e)}"

def listar_notas(quantidade=5):
    """Lista as últimas notas criadas."""
    pasta_notas = os.path.join(PASTA_NATY, "Notas")
    if not os.path.exists(pasta_notas):
        return "Você ainda não tem nenhuma nota salva, Natalia."

    arquivos = sorted(
        [f for f in os.listdir(pasta_notas) if f.endswith(".txt")],
        reverse=True
    )[:quantidade]

    if not arquivos:
        return "Nenhuma nota encontrada."

    return f"Suas últimas {len(arquivos)} notas: " + ", ".join(
        [f.replace("nota_", "").replace(".txt", "") for f in arquivos]
    )

def abrir_pasta_naty():
    """Abre a pasta Naty no Explorer."""
    import subprocess
    _garantir_pasta()
    subprocess.Popen(f'explorer "{PASTA_NATY}"', shell=True)
    return "Abrindo sua pasta Naty no Explorer."
