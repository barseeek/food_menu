import pprint

from environs import Env
import requests
import re
from googletrans import Translator


env = Env()
env.read_env()

FS_TOKEN = env.str('FS_TOKEN')

translator = Translator()


def fetch_product_calories(title, unit):
    initial_unit = unit
    initial_title = title
    title = re.sub(r'\([^)]*\)', '', title)
    if 'без' in title:
        title = title.split('без')[0].strip()
    words = title.split()
    if len(words) >= 2:
        last_two_words = words[-2:]
        title = ' '.join(last_two_words)
    if title.endswith('ы') and len(title.split()) == 1:
        title = title[:-1]

    translation = translator.translate(title, src='ru', dest='en').text
    units = {'чай': ['tsp'], 'стол': ['tbsp'], 'шт': ['serving', 'slice', translation, 'cereal'], 'стакан': ['cup',]}
    units_to_find = ['100g']
    for key in units.keys():
        if key in initial_unit.lower():
            units_to_find = units[key]

    url = 'https://platform.fatsecret.com/rest/server.api'
    headers = {'Authorization': f'Bearer {FS_TOKEN}'}
    params = {'method': 'foods.search', 'max_results': 25,
              'search_expression': translation, 'format': 'json'}
    try:
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
    except Exception as e:
        return e
    else:
        answer = response.json()
        #pprint.pprint(answer)
        if int(answer['foods']['total_results']) > 0:
            foods = answer['foods']['food']

            unit = 'г'
            if int(answer['foods']['total_results']) == 1:
                food_description = foods['food_description']
            else:
                food_description = foods[0]['food_description']

                found_match = False
                for food in foods:
                    for unit_to_find in units_to_find:
                        if unit_to_find.lower() in food['food_description']:

                            food_description = food['food_description']
                            unit = initial_unit
                            found_match = True
                            break
                    if found_match:
                        break
            calories_match = re.search(r'Calories: (?P<calories>\d+)kcal', food_description)
            calories = int(calories_match.group('calories'))
            if '100g' in units_to_find:
                calories = calories / 100

            return {
                'title': initial_title,
                'calories': calories,
                'unit': unit
            }
        else:
            return {
                'title': initial_title,
                'calories': 0,
                'unit': 0
            }


if __name__ == '__main__':
    word = 'Апельсин'
    unit = '1 штука'
    calories = fetch_product_calories(word, unit)
    print(calories)


