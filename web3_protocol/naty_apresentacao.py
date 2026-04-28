import speech_recognition as sr
import pyttsx3
import time

# Configuração da Voz da Naty
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Tenta selecionar uma voz feminina em português se disponível
for voice in voices:
    if "brazil" in voice.name.lower() or "portuguese" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 180) # Velocidade da fala

def falar(texto):
    print(f"Naty: {texto}")
    engine.say(texto)
    engine.runAndWait()

def apresentar_projeto():
    falar("Olá! Eu sou a Naty, sua assistente pessoal. É um prazer apresentar este protocolo Web3 desenvolvido para a Fase 2 Avançada.")
    time.sleep(1)
    falar("O projeto consiste em um ecossistema completo de incentivos descentralizados.")
    
    falar("Primeiro, temos o Naty Token, um ERC-20 utilitário que serve como combustível do sistema.")
    falar("Desenvolvemos também um contrato de Staking inteligente. Ele utiliza oráculos da Chainlink para buscar o preço do ETH em tempo real e ajustar as recompensas dos usuários.")
    
    falar("Para engajamento, criamos o Naty NFT, onde apoiadores podem mintar colecionáveis exclusivos diretamente pela interface.")
    
    falar("Por fim, implementamos a Naty DAO. Uma organização autônoma onde apenas quem tem tokens em stake pode votar em propostas de melhoria, garantindo uma governança justa.")
    
    falar("Todo o código foi auditado contra reentrância e está operando agora mesmo na rede de teste Sepolia. O frontend que você está vendo integra todos esses contratos de forma fluida.")
    
    falar("Estou pronta para mostrar qualquer parte do código ou realizar um teste ao vivo. O que deseja ver agora?")

def ouvir_comando():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Aguardando comando: 'Naty, fale sobre o projeto']...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        comando = r.recognize_google(audio, language='pt-BR').lower()
        print(f"Você disse: {comando}")
        if "naty" in comando and "projeto" in comando:
            apresentar_projeto()
        else:
            print("Comando não reconhecido. Tente dizer 'Naty, fale sobre o projeto'.")
    except Exception as e:
        print("Não consegui ouvir bem...")

if __name__ == "__main__":
    # Início do loop
    while True:
        ouvir_comando()
        time.sleep(1)
