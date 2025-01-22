from glados_brain import glados, get_response
import json
import os

user_input = "Please turn the outlet on in the kitchen please"

# Função para carregar JSON genérico
def load_json(file_path, default_data):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return default_data

get_response(user_input)


msg_reader =  load_json("response.json", "Not worked LOL")

print (f"This variable is the type: {type(msg_reader)}")

print (f"message to be readed:\n {msg_reader['message']} \n**********************")

try :
  glados.speak(msg_reader["message"], True)
  
except Exception as e:
  glados.speak("I'm being serious, I think there's something reeally wrong with me.", True)

