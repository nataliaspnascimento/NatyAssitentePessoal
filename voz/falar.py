import asyncio
import os
import tempfile
import threading
import pygame

_lock = threading.Lock()

# Voz neural da Microsoft (fluida e natural)
VOZ = "pt-BR-FranciscaNeural"

async def _gerar_audio_async(texto, caminho):
    import edge_tts
    communicate = edge_tts.Communicate(texto, VOZ, rate="+5%", volume="+10%")
    await communicate.save(caminho)

def falar(texto):
    """Fala com a voz neural da Microsoft (Francisca - pt-BR).
    Fluida, natural e sem sotaque robótico."""
    print(f"Naty diz: {texto}")

    with _lock:
        caminho_mp3 = None
        try:
            # Cria arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                caminho_mp3 = tmp.name

            # Gera áudio com edge-tts (neural)
            asyncio.run(_gerar_audio_async(texto, caminho_mp3))

            # Toca com pygame
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            pygame.mixer.music.load(caminho_mp3)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(15)

            pygame.mixer.music.unload()
            pygame.mixer.quit()

        except Exception as e:
            print(f"[ERRO VOZ NEURAL] {e}")
            # Fallback: gTTS
            try:
                from gtts import gTTS
                tts = gTTS(text=texto, lang='pt-br', slow=False)
                tts.save(caminho_mp3)
                pygame.mixer.init()
                pygame.mixer.music.load(caminho_mp3)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.quit()
            except Exception as e2:
                print(f"[ERRO VOZ FALLBACK] {e2}")
        finally:
            try:
                if caminho_mp3 and os.path.exists(caminho_mp3):
                    os.remove(caminho_mp3)
            except:
                pass
