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

# Инициализируем счетчик для анализа первых 30 строк
counter = 0

# Итерируемся по всем элементам в JSON
for item in existing_data:
    if 'eth_gtbbIndexResponce' not in item:
        rpc_urls = item.get('rpc', [])
        for rpc_url in rpc_urls:
            try:
                # Формируем RPC-запрос
                payload = {
                    "jsonrpc": "2.0",
                    "method": "eth_getTransactionByBlockNumberAndIndex",
                    "params": ["0x1", "0x0"],
                    "id": 1
                }
                headers = {'Content-Type': 'application/json'}
                
                # Выполняем запрос
                response = requests.post(rpc_url, json=payload, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    item['eth_gtbbIndexResponce'] = response.json()
                    print(f"Successfully fetched data for chainId {item['chainId']}")
                else:
                    item['eth_gtbbIndexResponce'] = f"Failed with status code {response.status_code}"
                    print(f"Failed to fetch data for chainId {item['chainId']}")
                
                break  # Выход из цикла после первого успешного/неуспешного запроса
            except requests.exceptions.RequestException as e:
                item['eth_gtbbIndexResponce'] = f"Connection error: {str(e)}"
                print(f"Connection error for chainId {item['chainId']}: {str(e)}")
        
        # Увеличиваем счетчик и проверяем, не достигли ли мы 30
        counter += 1
        if counter >= 5:
            break

# Сохраняем обновленные данные в файл
save_data_to_file(existing_data, "sites.json")
