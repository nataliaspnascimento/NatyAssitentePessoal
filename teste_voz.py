import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print("--- VOZES DISPONÍVEIS ---")
for index, voice in enumerate(voices):
    print(f"{index}: {voice.name} | ID: {voice.id}")

print("\nTestando a melhor voz em português encontrada...")
for voice in voices:
    if "portuguese" in voice.name.lower() or "brazil" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        print(f"Usando: {voice.name}")
        engine.say("Olá Natalia! Estou testando minha voz. Você consegue me ouvir?")
        engine.runAndWait()
        break
else:
    print("Nenhuma voz em português encontrada.")
