import json
import os
import requests

# Функция для загрузки существующих данных из файла
def load_existing_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

# Функция для сохранения данных в файл
def save_data_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Загружаем существующие данные
existing_data = load_existing_data("sites.json")

# Итерируемся по всем элементам в JSON
for item in existing_data:
    # Пропускаем элементы, где уже есть blockNumber
    if 'blockNumber' in item:
        continue

    # Удаляем блок с eth_gtbbIndexResponce, если он есть
    if 'eth_gtbbIndexResponce' in item:
        del item['eth_gtbbIndexResponce']

    rpc_urls = item.get('rpc', [])
    if not rpc_urls:
        item['blockNumber'] = "No RPC URL available"
        continue

    # Подготовка RPC запроса для получения номера последнего блока
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }

    headers = {'Content-Type': 'application/json'}

    # Выполнение запроса (пытаемся только один раз)
    try:
        response = requests.post(rpc_urls[0], json=payload, headers=headers, timeout=5)
        hex_block_number = response.json().get('result', 'Unknown')
        if hex_block_number != 'Unknown' and isinstance(hex_block_number, str):
            item['blockNumber'] = int(hex_block_number, 16)
        else:
            item['blockNumber'] = 'Unknown'
    except requests.exceptions.RequestException as e:
        item['blockNumber'] = f"Error: {str(e)}"

    # Сохраняем обновленные данные в файл на каждой итерации
    save_data_to_file(existing_data, "sites.json")
