import json
import os

# Caminhos dos arquivos JSON
DEVICE_FILE = "devices.json"
LOCATION_FILE = "locations.json"
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

# Função para cadastrar um dispositivo
def register_device(device_id, device_type, location, custom_name):
    devices = load_json(DEVICE_FILE, {"devices": []})
    device_types = load_json(DEVICE_TYPES_FILE, {"types": []})
    locations = load_json(LOCATION_FILE, {"locations": []})

    # Verificar se o tipo de dispositivo é válido
    if device_type not in device_types["types"]:
        print(f"Tipo de dispositivo '{device_type}' não é válido.")
        return

    # Adicionar localização se não existir
    if location not in locations["locations"]:
        locations["locations"].append(location)
        save_json(LOCATION_FILE, locations)

    # Verificar se o dispositivo já está registrado
    for device in devices["devices"]:
        if device["id"] == device_id:
            print(f"Dispositivo com ID '{device_id}' já está registrado.")
            return

    # Adicionar o novo dispositivo
    new_device = {
        "id": device_id,
        "type": device_type,
        "location": location,
        "custom_name": custom_name
    }
    devices["devices"].append(new_device)
    save_json(DEVICE_FILE, devices)
    print(f"Dispositivo com ID '{device_id}' registrado com sucesso.")

# Função para listar dispositivos
def list_devices():
    devices = load_json(DEVICE_FILE, {"devices": []})["devices"]
    if not devices:
        print("Nenhum dispositivo registrado.")
        return

    for device in devices:
        print(f"ID: {device['id']}, Tipo: {device['type']}, Localização: {device['location']}, Nome Personalizado: {device['custom_name']}")

# Exemplo de uso
if __name__ == "__main__":
    # Adicionar tipos de dispositivos e localizações iniciais
    save_json(DEVICE_TYPES_FILE, {"types": ["light", "outlet", "camera", "smartlock"]})
    save_json(LOCATION_FILE, {"locations": ["sala", "quarto", "cozinha", "estúdio", "escritório"]})

    # Registrar dispositivos
    register_device("device_1", "light", "sala", "Luz da Sala")
    register_device("device_2", "outlet", "cozinha", "Tomada da Cozinha")

    # Listar dispositivos
    list_devices()
