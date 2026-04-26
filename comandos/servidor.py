import os
import subprocess

def conectar_ssh(config):
    """
    Abre um novo terminal SSH para o servidor configurado.
    """
    # Tenta pegar as informações da config ou usa um padrão para perguntar
    usuario = config.get("ssh_user", "usuario")
    ip = config.get("ssh_ip", "192.168.1.100") # Exemplo
    
    try:
        # Abre o Windows Terminal ou CMD com o comando SSH
        # Usamos 'start' para abrir em uma janela separada
        comando = f'start cmd /k "ssh {usuario}@{ip}"'
        os.system(comando)
        return f"Abrindo terminal SSH para Natalia em {ip}. Por favor, verifique a nova janela."
    except Exception as e:
        return f"Não consegui iniciar a conexão SSH: {str(e)}"

def abrir_pasta_servidor():
    """
    Tenta abrir a pasta do servidor via rede (samba) se configurado.
    """
    # Exemplo de caminho de rede
    caminho = r"\\SERVIDOR_UBUNTU\arquivos" 
    try:
        os.startfile(caminho)
        return "Abrindo a pasta do servidor na rede."
    except:
        return "Não consegui acessar a pasta do servidor. Verifique se o Samba está ativo no Ubuntu."
