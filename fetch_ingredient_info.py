import pprint

from environs import Env
import requests
import re
from googletrans import Translator


env = Env()
env.read_env()

SPOONACULAR_KEY = env.str('SPOONACULAR_KEY')

translator = Translator()

rus_allergies = [
    'Рыба и морепродукты',
    'Зерновые',
    'Продукты пчеловодства',
    'Орехи и бобовые ',
    'Молочные продукты'
]
intolerances = [
    ['fish', 'shellfish', 'seafood'],
    ['wheat', 'grain', 'gluten'],
    ['honey',],
    ['nut', 'peanut', 'tree nut', 'sesame'],
    ['dairy', 'milk', 'cheese', 'yogurt']
]

intolerances_dict = dict(zip(rus_allergies, intolerances))


def fetch_ingredient_info(title, amount, unit):
    initial_unit = unit
    initial_title = title
    title = re.sub(r'\([^)]*\)', '', title)
    title = re.sub(r'\b\w*ий\b', '', title)
    if 'без' in title:
        title = title.split('без')[0].strip()
    words = title.split()
    if len(words) >= 2:
        last_two_words = words[-2:]
        title = ' '.join(last_two_words)
    translated_title = translator.translate(title, src='ru', dest='en').text
    translated_unit = translator.translate(unit, src='ru', dest='en').text
    headers = {'Content-Type': 'application/json'}

    search_url = 'https://api.spoonacular.com/food/ingredients/search'
    params = {'query': translated_title, 'apiKey': SPOONACULAR_KEY, 'number': 1}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    response_json = response.json()
    print(response_json)
    if not response_json['totalResults'] == 0:
        ingredient_id = response_json['results'][0]['id']
    else:
        print(translated_title)
        try:
            translated_title = translated_title.split(' ', 1)[1]
            params = {'query': translated_title, 'apiKey': SPOONACULAR_KEY,
                      'number': 1}
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            response_json = response.json()
            ingredient_id = response_json['results'][0]['id']
        except Exception as e:
            ingredient_breakdown = {
                'title': initial_title,
                'units_amount': f'{amount} {initial_unit}',
                'calories': 0,
                'intolerance': 'Проверить!'
            }
            return ingredient_breakdown

    ingredient_url = f'https://api.spoonacular.com/food/ingredients/{ingredient_id}/information'
    params = {'amount': amount, 'unit': translated_unit, 'apiKey': SPOONACULAR_KEY}

    response = requests.get(ingredient_url, headers=headers, params=params)
    response.raise_for_status()
    response_json = response.json()

    pprint.pprint(response_json)

    ingredient_breakdown = {
        'title': initial_title,
        'units_amount': f'{amount} {initial_unit}',
        'calories': find_calories(response_json),
        'intolerance': find_intolerance(response_json)
    }
    return ingredient_breakdown


def find_calories(response_json):
    for nutrient in response_json['nutrition']['nutrients']:
        if nutrient['name'] == 'Calories':
            calories = nutrient['amount']
            return calories

    return


def find_intolerance(response_json):
    fields_to_check = ['originalName', 'original', 'name']

    for rus_intolerance, intolerances in intolerances_dict.items():
        for intolerance in intolerances:
            for category in response_json['categoryPath']:
                if intolerance in category:
                    return rus_intolerance
            else:
                for field in fields_to_check:
                    if intolerance in response_json[field]:
                        return rus_intolerance

    return


if __name__ == '__main__':
    title = 'Кета'
    amount = 100
    unit = 'г'
    info = fetch_ingredient_info(title, amount, unit)

    pprint.pprint(info)
