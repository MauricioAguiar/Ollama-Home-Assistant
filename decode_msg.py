import json
from tuya_iot import TuyaOpenAPI
import time
import os

from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, USERNAME, PASSWORD

# Configurações do Tuya API

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect(USERNAME, PASSWORD, "1", "smartlife")

# Caminhos dos arquivos JSON
DEVICE_FILE = "devices.json"
POSITIONS_FILE = "positions.json"
DEVICE_TYPES_FILE = "device_types.json"

# Função para carregar JSON genérico
def load_json(file_path, default_data):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return default_data

# Função para salvar JSON genérico
def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Função para configurar luz piscante
def set_blinking_light(device_id, hue, saturation, brightness, duration, blink_interval):
    light_command = {
        'commands': [
            {'code': 'color_set', 'value': {'h': hue, 's': saturation, 'v': brightness}}
        ]
    }

    end_time = time.time() + duration
    while time.time() < end_time:
        openapi.post(f'/v1.0/devices/{device_id}/commands', light_command)
        time.sleep(blink_interval)
        off_command = {'commands': [{'code': 'switch_led', 'value': False}]}
        openapi.post(f'/v1.0/devices/{device_id}/commands', off_command)
        time.sleep(blink_interval)

# Função para ligar ou desligar dispositivos por localização
def toggle_devices_by_location(location, action):
    devices = load_json(DEVICE_FILE, {"devices": []})["devices"]
    found = False

    for device in devices:
        if device["position"] == location:
            found = True
            device_type = device["type"]
            command = None

            if device_type == "light":
                command = {"commands": [{"code": "switch_led", "value": action}]}
            elif device_type == "outlet":
                command = {"commands": [{"code": "switch_1", "value": action}]}
            else:
                print(f"Tipo de dispositivo '{device_type}' não suportado para a ação.")

            if command:
                openapi.post(f'/v1.0/devices/{device["id"]}/commands', command)
                print(f"O dispositivo {device['id']} ({device_type}) em {location} mudou o status de ligado para {action}")

    if not found:
        print(f"Nenhum dispositivo encontrado na localização '{location}'.")

# Mapeamento de ações para funções
action_map = {
    "set_blinking_light": set_blinking_light,
    "toggle_devices_by_location": toggle_devices_by_location
}

# Teste de integração com o TuyaSmart
def ligar_tomada():
    device_id = "eb9610e0090907ba73eh5f"  # ID do dispositivo listado
    tuya_command = {
    "commands": [{"code": "switch_1", "value": False}]  # Liga o dispositivo
    }
    openapi.post(f"/v1.0/devices/{device_id}/commands", tuya_command)
    print(f"Comando enviado para o dispositivo {device_id}")
    print ("Teste bem sucedido ate agr")

# Função para processar JSON e executar a ação
def process_command(json_command):
    try:
        # Parse do JSON
        command = json.loads(json_command)
        action = command.get("action")
        parameters = command.get("parameters", {})

        # Verificar se a ação existe no mapeamento
        if action in action_map:
            # Chamar a função correspondente
            action_map[action](**parameters)
        else:
            print(f"Ação '{action}' não reconhecida.")
    except Exception as e:
        print(f"Erro ao processar comando: {e}")

# Exemplo de JSON recebido
json_input = '''
{
    "action": "set_blinking_light",
    "parameters": {
        "device_id": "id_do_dispositivo",
        "hue": 0,
        "saturation": 100,
        "brightness": 10,
        "duration": 10,
        "blink_interval": 0.5
    }
}
'''

# Processar e executar o comando
process_command(json_input)

# Exemplo de JSON para ligar todos os dispositivos em uma localização
json_toggle = '''
{
    "action": "toggle_devices_by_location",
    "parameters": {
        "location": "cozinha",
        "action": false
    }
}
'''

# Processar e executar o comando
process_command(json_toggle)
#ligar_tomada()