import speech_recognition as sr
import numpy as np

# Reconhecedor global (criado uma vez, não toda vez que ouve)
_reconhecedor = sr.Recognizer()
_reconhecedor.energy_threshold = 300       # Sensibilidade fixa (mais rápido)
_reconhecedor.dynamic_energy_threshold = True
_reconhecedor.pause_threshold = 0.8        # Para de ouvir 0.8s após silêncio

def detectar_frequencia(audio_data):
    """Estima a frequência vocal para identificar o usuário."""
    try:
        raw_data = audio_data.get_raw_data(convert_rate=16000, convert_width=2)
        samples = np.frombuffer(raw_data, dtype=np.int16).astype(float)
        if len(samples) == 0:
            return 0.0
        zero_crossings = np.where(np.diff(np.sign(samples)))[0]
        frequencia = len(zero_crossings) * (16000 / (2 * len(samples)))
        return float(frequencia)
    except:
        return 0.0

def ouvir():
    """
    Escuta o microfone e retorna (texto, frequencia).
    Otimizado para resposta rápida.
    """
    with sr.Microphone() as source:
        # Ajuste de ruído apenas na primeira vez (rápido)
        _reconhecedor.adjust_for_ambient_noise(source, duration=0.3)
        print("Ouvindo...")

        try:
            audio = _reconhecedor.listen(source, timeout=6, phrase_time_limit=8)
            print("Processando...")
            texto = _reconhecedor.recognize_google(audio, language='pt-BR')
            print(f"Você disse: {texto}")
            frequencia = detectar_frequencia(audio)
            return texto, frequencia

        except sr.WaitTimeoutError:
            return None, 0.0
        except sr.UnknownValueError:
            return None, 0.0
        except Exception as e:
            print(f"[ERRO AUDIO] {e}")
            return None, 0.0
