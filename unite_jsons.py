import glob
import json


if __name__ == '__main__':
    files = glob.glob('recipies_database_part_*.json')
    all_data = []

    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            all_data.extend(data)

    json_str = json.dumps(all_data, indent=4, ensure_ascii=False)
    with open('combined_recipies.json', 'w', encoding='utf-8') as f:
        f.write(json_str)
