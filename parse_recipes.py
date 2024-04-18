from urllib.parse import urljoin, urlsplit
import json
import requests
from bs4 import BeautifulSoup
import ftfy


if __name__ == '__main__':
    base_url = 'https://eda.ru/'
    diets = ['', 'keto-dieta', 'vegetarianskaya-eda', 'nizkokaloriynaya-eda']
    rus_diets = ['Классическое', 'Кето', 'Вегетарианское', 'Низкоуглеводное']
    zipped_diets = dict(zip(diets, rus_diets))
    meals = ['zavtraki', 'supy', 'osnovnye-blyuda', 'vypechka-deserty']
    rus_categories = ['Завтраки', 'Обеды', 'Ужины', 'Десерты']
    zipped_meals = dict(zip(meals, rus_categories))
    links = [
        urljoin(base_url, f'recepty/{diet}/{meal}') for meal in meals for diet in diets
    ]
    recipies = []
    for link in links[:2]:
        try:
            response = requests.get(link)
            response.raise_for_status()
        except Exception as e:
            print(e)
        else:
            soup = BeautifulSoup(response.text, 'lxml')
            selector = "div.emotion-1j5xcrd a[href^='/recepty']"
            recipies_paths = [a['href'] for a in soup.select(selector)]

            for recipe_path in recipies_paths[:4]:
                recipe_url = urljoin(base_url, recipe_path)
                try:
                    response = requests.get(recipe_url)
                    response.raise_for_status()
                except Exception as e:
                    print(e)
                else:
                    soup = BeautifulSoup(response.text, 'lxml')

                    title = soup.find('h1', class_='emotion-gl52ge').text
                    title = ftfy.fix_text(title)

                    image = soup.find('img', class_='emotion-gxbcya').get('src')

                    description = [post.text for post in soup.select('div.emotion-13pa6yw span.emotion-wdt5in')]
                    description = '\n'.join(description)
                    description = ftfy.fix_text(description)

                    category = urlsplit(recipe_url).path.split('/')[2]
                    category = zipped_meals[category]

                    path_parts = urlsplit(link).path.split('/')
                    menu = path_parts[2] if len(path_parts) > 3 else ''
                    menu = zipped_diets[menu]

                    ingredients_titles = [title.text for title in soup.select('span.emotion-mdupit')]
                    ingredients_units = [unit.text for unit in soup.select('span.emotion-bsdd3p')]
                    ingredients = dict(zip(ingredients_titles, ingredients_units))

                    parsed_recipe = {
                        'title': title,
                        'image': image,
                        'description': description,
                        'category': category,
                        'menu': menu,
                        'ingredients': ingredients
                    }
                    recipies.append(parsed_recipe)

    json_str = json.dumps(recipies, indent=4, ensure_ascii=False)
    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(json_str)