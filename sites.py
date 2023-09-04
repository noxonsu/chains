import requests
import json
import os

# Функция для загрузки существующих данных из sites.json
def load_existing_sites(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

# Функция для сохранения данных в sites.json
def save_sites(filename, sites):
    with open(filename, 'w') as f:
        json.dump(sites, f, indent=4)

# URL для скачивания исходного JSON
url = "https://chainid.network/chains.json"

# Загрузка существующих данных
existing_sites = load_existing_sites('sites.json')

# Скачивание исходного JSON
response = requests.get(url)
if response.status_code == 200:
    data = json.loads(response.text)
    
    # Инициализация списка для новых сайтов
    new_sites = []
    
    for item in data:
        # Формирование словаря с нужными полями
        site = {
            'chainId': item.get('chainId', ''),
            'url': item.get('infoURL', ''),
            'ticker': item.get('nativeCurrency', {}).get('symbol', ''),
            'comment': ''  # Поле для комментариев, пока оставляем пустым
        }
        
        # Проверка на дубликаты и существующие записи
        if site not in existing_sites and site not in new_sites:
            new_sites.append(site)
    
    # Объединение существующих и новых сайтов
    all_sites = existing_sites + new_sites
    
    # Сохранение в sites.json
    save_sites('sites.json', all_sites)
    
    print(f"Added {len(new_sites)} new sites.")
else:
    print(f"Failed to download JSON. Status code: {response.status_code}")
