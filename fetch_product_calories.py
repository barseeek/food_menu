from environs import Env
import requests
import re
from googletrans import Translator


env = Env()
env.read_env()

FS_TOKEN = env.str('FS_TOKEN')


def fetch_product_calories(title):
    translator = Translator()
    translation = translator.translate(title, src='ru', dest='en').text
    url = 'https://platform.fatsecret.com/rest/server.api'
    headers = {'Authorization': f'Bearer {FS_TOKEN}'}
    params = {'method': 'foods.search', 'max_results': 1,
              'search_expression': translation, 'format': 'json'}
    response = requests.post(url, headers=headers, params=params)
    response.raise_for_status()
    answer = response.json()
    food_description = answer['foods']['food']['food_description']
    calories_match = re.search(r'Calories: (?P<calories>\d+)kcal', food_description)
    calories = int(calories_match.group('calories'))

    return {title: calories}


if __name__ == '__main__':
    word = 'Сушеный розмарин'

    calories = fetch_product_calories(word)
    print(calories)

