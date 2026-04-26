import os
import psutil
import time
import ctypes

# Para controle de volume via Windows API
WM_APPCOMMAND = 0x319
APPCOMMAND_VOLUME_UP = 0x0A
APPCOMMAND_VOLUME_DOWN = 0x09
APPCOMMAND_VOLUME_MUTE = 0x08

def controlar_volume(acao):
    """
    Controla o volume do Windows.
    acao: 'aumentar', 'diminuir', 'mudo'
    """
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    if acao == "aumentar":
        for _ in range(5): # Aumenta 10% (cada passo é 2%)
            ctypes.windll.user32.SendMessageW(hwnd, WM_APPCOMMAND, 0, APPCOMMAND_VOLUME_UP << 16)
        return "Volume aumentado, Natalia."
    elif acao == "diminuir":
        for _ in range(5):
            ctypes.windll.user32.SendMessageW(hwnd, WM_APPCOMMAND, 0, APPCOMMAND_VOLUME_DOWN << 16)
        return "Volume diminuído."
    elif acao == "mudo":
        ctypes.windll.user32.SendMessageW(hwnd, WM_APPCOMMAND, 0, APPCOMMAND_VOLUME_MUTE << 16)
        return "Volume alternado para mudo."

def obter_saude_pc():
    """
    Retorna status de CPU e RAM.
    """
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return f"Seu computador está operando bem. O uso de CPU está em {cpu}% e a memória RAM em {ram}%."

def gerenciar_energia(acao, tempo_minutos=0):
    """
    Desliga ou reinicia o PC.
    """
    tempo_segundos = tempo_minutos * 60
    if acao == "desligar":
        os.system(f"shutdown /s /t {tempo_segundos}")
        if tempo_minutos > 0:
            return f"Entendido. Programando desligamento para daqui a {tempo_minutos} minutos. Até logo, Natalia."
        else:
            return "Desligando agora. Adeus, Natalia."
    elif acao == "cancelar":
        os.system("shutdown /a")
        return "Desligamento agendado foi cancelado."
    
def obter_ip():
    import socket
    hostname = socket.gethostname()
    ip_local = socket.gethostbyname(hostname)
    return f"O seu endereço IP local é {ip_local}."
