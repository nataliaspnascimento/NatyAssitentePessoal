import os
import shutil
from pathlib import Path

def organizar_desktop():
    """
    Move arquivos da Área de Trabalho para pastas organizadas por extensão.
    """
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    pastas = {
        "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
        "Documentos": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".csv"],
        "Instaladores": [".exe", ".msi"],
        "Compactados": [".zip", ".rar", ".7z"],
        "Videos": [".mp4", ".mkv", ".mov", ".avi"]
    }

    try:
        contagem = 0
        for arquivo in os.listdir(desktop):
            caminho_completo = os.path.join(desktop, arquivo)
            
            if os.path.isfile(caminho_completo):
                extensao = Path(arquivo).suffix.lower()
                
                for pasta, extensoes in pastas.items():
                    if extensao in extensoes:
                        pasta_destino = os.path.join(desktop, pasta)
                        
                        if not os.path.exists(pasta_destino):
                            os.makedirs(pasta_destino)
                        
                        shutil.move(caminho_completo, os.path.join(pasta_destino, arquivo))
                        contagem += 1
                        break
        
        if contagem > 0:
            return f"Organizei {contagem} arquivos na sua área de trabalho, Natalia."
        else:
            return "Sua área de trabalho já está organizada, Natalia."
    except Exception as e:
        return f"Tive um erro ao organizar os arquivos: {str(e)}"

def criar_pasta(nome):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    caminho = os.path.join(desktop, nome)
    try:
        os.makedirs(caminho, exist_ok=True)
        return f"Pasta '{nome}' criada com sucesso na área de trabalho."
    except Exception as e:
        return f"Erro ao criar pasta: {str(e)}"
