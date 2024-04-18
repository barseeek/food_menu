import pprint

from environs import Env
import requests
import re
from googletrans import Translator


env = Env()
env.read_env()

FS_TOKEN = env.str('FS_TOKEN')


def fetch_product_calories(title, unit):
    initial_unit = unit
    initial_title = title
    words = title.split()
    if len(words) >= 2:
        last_two_words = words[-2:]
        title = ' '.join(last_two_words)

    translator = Translator()
    translation = translator.translate(title, src='ru', dest='en').text
    units = {'чай': ['tsp'], 'стол': ['tbsp'], 'шт': ['serving', 'slice', translation], 'стакан': ['cup',]}
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
                print(food_description)
                found_match = False
                for food in foods:
                    for unit_to_find in units_to_find:
                        if unit_to_find.lower() in food['food_description']:
                            print(1)
                            food_description = food['food_description']
                            unit = initial_unit
                            found_match = True
                            break
                    if found_match:
                        break
            calories_match = re.search(r'Calories: (?P<calories>\d+)kcal', food_description)
            calories = int(calories_match.group('calories'))
            if 'г' in unit.lower():
                calories = calories / 100

            return {initial_title: [calories, unit]}
        else:
            return {initial_title: [0, '0']}


if __name__ == '__main__':
    word = 'Мягкий творог'
    unit = '200 г'
    calories = fetch_product_calories(word, unit)
    print(calories)


