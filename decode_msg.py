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
LOCATIONS_FILE = "locations.json"
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
def set_light(device_id, hue, saturation, brightness, duration, blink_interval):
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

# Função genérica para alternar dispositivos com base em critérios
def toggle_devices(filter_key, filter_value, action):
    devices = load_json(DEVICE_FILE, {"devices": []})["devices"]
    found = False

    for device in devices:

        if device.get(filter_key).strip().lower() == filter_value.lower().strip():
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
                print(f"O dispositivo {device['id']} ({device_type}) com {filter_key} = {filter_value.strip()} mudou o status para {action}")

    if not found:
        print(f"Nenhum dispositivo encontrado com {filter_key} = '{filter_value}'.")

# Função para ligar ou desligar dispositivos por tipo
def toggle_devices_by_type(device_type, action):
    toggle_devices("type", device_type, action)
    
# Exemplo de uso para nome personalizado
def toggle_devices_by_custom_name(custom_name, action):
    toggle_devices("custom_name", custom_name, action)
    
# Exemplo de uso para localização
def toggle_devices_by_location(location, action):
    toggle_devices("location", location, action)

# Mapeamento de ações para funções
action_map = {
    "set_blinking_light": set_light,
    "toggle_devices_by_location": toggle_devices_by_location,
    "toggle_devices_by_custom_name" : toggle_devices_by_custom_name,
    "toggle_devices_by_type" : toggle_devices_by_type
}

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
    "action": "set_light",
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
# process_command(json_input)

# Exemplo de JSON para ligar todos os dispositivos em uma localização
json_toggle = '''
{
    "action": "toggle_devices_by_custom_name",
    "parameters": {
        "custom_name": "tomada",
        "action": false
    }
}
'''

# Processar e executar o comando
   

process_command(json_toggle)

#ligar_tomada()