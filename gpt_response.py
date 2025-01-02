from ollama import chat
from ollama import ChatResponse
import json


response: ChatResponse = chat(model="GlaDos", messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
#print(response.message.content)

# Função para salvar JSON genérico
def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        
        
save_json("response.json", response.message.content)