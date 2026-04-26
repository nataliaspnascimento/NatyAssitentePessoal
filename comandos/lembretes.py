import threading
import time
from tkinter import messagebox
import winsound

def agendar_lembrete(tarefa, tempo_texto, falar_func):
    """
    Agenda um lembrete. 
    tempo_texto: '10 minutos', '1 hora', '30 segundos'
    """
    try:
        # Extrai o número e a unidade
        partes = tempo_texto.split()
        valor = int(partes[0])
        unidade = partes[1].lower()

        if "hora" in unidade:
            segundos = valor * 3600
        elif "minuto" in unidade:
            segundos = valor * 60
        else:
            segundos = valor

        def aviso():
            time.sleep(segundos)
            # Alerta Sonoro
            winsound.Beep(1000, 500)
            winsound.Beep(1200, 500)
            
            # Alerta de Voz
            falar_func(f"Natalia, aqui está o seu lembrete: {tarefa}")
            
            # Alerta Visual (Messagebox em Thread separada para não travar)
            messagebox.showinfo("Lembrete da Naty", f"Natalia, você me pediu para te lembrar: \n\n {tarefa}")

        # Inicia o temporizador em uma thread separada para não travar a Naty
        threading.Thread(target=aviso, daemon=True).start()
        
        return f"Tudo bem, Natalia. Vou te lembrar de '{tarefa}' daqui a {tempo_texto}."
    except Exception as e:
        return "Não consegui entender o tempo do lembrete. Tente falar 'número + unidade', por exemplo: '10 minutos'."
