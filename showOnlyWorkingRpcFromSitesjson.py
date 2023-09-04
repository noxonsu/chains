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

# Инициализируем список для новых данных
new_data = []

# Итерируемся по всем элементам в JSON
for item in existing_data:
    if 'eth_gtbbIndexResponce' not in item or not item['eth_gtbbIndexResponce'] or (isinstance(item['eth_gtbbIndexResponce'], dict) and item['eth_gtbbIndexResponce'].get('jsonrpc') == '2.0'):
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

        # Выполнение запроса
        try:
            response = requests.post(rpc_urls[0], json=payload, headers=headers, timeout=30)
            hex_block_number = response.json().get('result', 'Unknown')
            if hex_block_number != 'Unknown' and isinstance(hex_block_number, str):
                item['blockNumber'] = int(hex_block_number, 16)
            else:
                item['blockNumber'] = 'Unknown'
        except requests.exceptions.RequestException as e:
            item['blockNumber'] = f"Error: {str(e)}"

        new_data.append(item)
        
        # Сохраняем новые данные в файл на каждой итерации
        save_data_to_file(new_data, "sites_with_working_rpc.json")
