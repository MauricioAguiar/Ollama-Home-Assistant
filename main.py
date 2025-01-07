import speech_recognition as sr
import pyttsx3
import webbrowser
import time
from datetime import datetime, timedelta
from tuya_iot import TuyaOpenAPI

from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, USERNAME, PASSWORD

# Configurações do Tuya API

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect(USERNAME, PASSWORD, "1", "smartlife")



# Inicializar o mecanismo de fala
engine = pyttsx3.init()
engine.setProperty("rate", 250)  # Velocidade da fala
engine.setProperty("volume", 0.9)  # Volume (0.0 a 1.0)

# Lista de tarefas
to_do_list = []

# Função para falar
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Função para ouvir
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Desculpe, não entendi. Por favor, repita.")
            return None
        except sr.RequestError:
            speak("Erro de rede. Verifique sua conexão.")
            return None
        except sr.WaitTimeoutError:
            speak("Nenhuma entrada detectada. Tente novamente.")
            return None

# Adicionar à lista de tarefas
def add_to_todo(task):
    to_do_list.append(task)
    speak(f"Adicionado {task} à sua lista de tarefas.")

# Mostrar lista de tarefas
def show_todo_list():
    if to_do_list:
        speak("Aqui está sua lista de tarefas:")
        for i, task in enumerate(to_do_list, 1):
            speak(f"{i}. {task}")
    else:
        speak("Sua lista de tarefas está vazia.")

# Pesquisa na web
def search_web(query):
    speak(f"Pesquisando na web por {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Configurar lembrete
def set_reminder(task, minutes):
    remind_time = datetime.now() + timedelta(minutes=minutes)
    speak(f"Vou te lembrar de {task} em {minutes} minutos.")
    while True:
        if datetime.now() >= remind_time:
            speak(f"Lembrete: {task}")
            break
        time.sleep(10)  # Verificar a cada 10 segundos

# Teste de integração com o TuyaSmart
def ligar_tomada():
    device_id = "eb9610e0090907ba73eh5f"  # ID do dispositivo listado
    tuya_command = {
    "commands": [{"code": "switch_1", "value": True}]  # Liga o dispositivo
    }
    openapi.post(f"/v1.0/devices/{device_id}/commands", tuya_command)
    print(f"Comando enviado para o dispositivo {device_id}")
    print ("Teste bem sucedido ate agr")

# Loop principal
def main():
    speak("Olá! Sou sua assistente. Como posso ajudar?")
    while True:
        command = listen()
        if command:
            if "adicionar à lista de tarefas" in command:
                speak("Qual tarefa você gostaria de adicionar?")
                task = listen()
                if task:
                    add_to_todo(task)

            elif "mostrar minha lista de tarefas" in command:
                show_todo_list()

            elif "pesquisar por" in command:
                query = command.replace("pesquisar por", "").strip()
                if query:
                    search_web(query)
                    
            elif "ligar tomada" in command:
                ligar_tomada()

            elif "definir um lembrete" in command:
                speak("Sobre o que devo te lembrar?")
                task = listen()
                if task:
                    speak("Em quantos minutos?")
                    try:
                        minutes = int(listen())
                        set_reminder(task, minutes)
                    except ValueError:
                        speak("Não entendi o tempo. Por favor, tente novamente.")

            elif "sair" in command or "fechar" in command:
                speak("Até logo!")
                break

            else:
                speak("Desculpe, não entendi esse comando.")

if __name__ == "__main__":
    main()
