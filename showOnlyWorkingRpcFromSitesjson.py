import json
import os

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

# Фильтруем данные
filtered_data = [item for item in existing_data if 'eth_gtbbIndexResponce' in item and item['eth_gtbbIndexResponce'].get('jsonrpc') == '2.0']

# Сохраняем отфильтрованные данные в новый файл
save_data_to_file(filtered_data, "sites_with_working_rpc.json")
