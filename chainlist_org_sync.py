import requests
import json
import os
from datetime import datetime  # Import the datetime library

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

# URL, откуда скачиваем JSON
url = "https://chainid.network/chains.json"

# Скачиваем JSON
response = requests.get(url)
if response.status_code == 200:
    # Парсим JSON
    data = json.loads(response.text)
    
    # Загружаем существующие данные
    existing_data = load_existing_data("sites.json")
    existing_chain_ids = {item['chainId'] for item in existing_data}
    
    # Инициализируем список для новых данных
    new_data = []
    
    # Итерируемся по всем элементам в JSON
    for item in data:
        chain_id = item.get('chainId', None)
        info_url = item.get('infoURL', None)
        ticker = item.get('nativeCurrency', {}).get('symbol', None)
        comment = item.get('name', None)
        rpc = item.get('rpc', [])
        
        # Проверяем на дубликаты и существующие записи
        if chain_id not in existing_chain_ids:
            current_datetime = datetime.now().isoformat()  # Get the current datetime in ISO format

            if 'testnet' not in info_url.lower() and 'testnet' not in comment.lower():
                new_data.append({
                    'chainId': chain_id,
                    'url': info_url,
                    'ticker': ticker,
                    'comment': comment,
                    'rpc': rpc,
                    'dateAdd': current_datetime  # Add the current datetime
                })
                existing_chain_ids.add(chain_id)
    
    # Сохраняем новые и существующие данные в файл
    save_data_to_file(existing_data + new_data, "sites.json")
    
    print(f"Saved {len(new_data)} new entries to sites.json.")
else:
    print(f"Failed to download JSON. Status code: {response.status_code}")
