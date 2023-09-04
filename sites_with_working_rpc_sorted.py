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
existing_data = load_existing_data("sites_with_working_rpc.json")

# Фильтруем и сортируем данные
filtered_data = []

for item in existing_data:
    block_number = item.get('blockNumber', None)
    name = item.get('comment', '').lower()
    url = item.get('url', '').lower()

    # Удаляем, если blockNumber не является числом или если в названии или URL есть слово "test"
    if isinstance(block_number, int) and 'test' not in name and 'test' not in url:
        filtered_data.append(item)

# Сортируем по blockNumber
sorted_data = sorted(filtered_data, key=lambda x: x['blockNumber'])

# Сохраняем отфильтрованные и отсортированные данные в файл
save_data_to_file(sorted_data, "sites_with_working_rpc_sorted.json")
