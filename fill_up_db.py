import json
import os
import requests
import django
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_menu.settings')
django.setup()

from orderapp.models import Meal, Menu, Product, Allergy, Ingredient, \
    Recipe

rus_allergies = [
    'Рыба и морепродукты',
    'Зерновые',
    'Продукты пчеловодства',
    'Орехи и бобовые ',
    'Молочные продукты'
]


def process_recipe(recipe_info):
    meal, created = Meal.objects.update_or_create(
        title=recipe_info['category']
    )
    menu, created = Menu.objects.update_or_create(
        title=recipe_info['menu']
    )
    recipe, created = Recipe.objects.update_or_create(
        title=recipe_info['title'],
        description=recipe_info['description'],
        meal=meal,
        menu=menu
    )

    for ingredient in recipe_info['ingredients']:
        if 'units_amount' in ingredient:
            ingredient['unit'] = ingredient['units_amount']
            del ingredient['units_amount']

        product, created = Product.objects.update_or_create(
            title=ingredient['title']
        )
        if ingredient['intolerance'] in rus_allergies:
            allergy, created = Allergy.objects.update_or_create(
                title=ingredient['intolerance']
            )
            product.allergy = allergy
        else:
            allergy, created = Allergy.objects.update_or_create(
                title='Нет'
            )
            product.allergy = allergy
        product.save()
        print(ingredient)
        Ingredient.objects.update_or_create(
            unit=ingredient['unit'],
            calories=round(ingredient['calories'], 1),
            product=product,
            recipe=recipe
        )

    ingredients = recipe.ingredients.all()
    calories = sum(ingredient.calories for ingredient in ingredients)
    recipe.calories = calories

    os.makedirs('media', exist_ok=True)
    try:
        response = requests.get(recipe_info['image'])
        response.raise_for_status()
    except Exception as err:
        print(err)
    else:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()
        recipe.image.save(os.path.basename(recipe_info['image']),
                          File(img_temp))
    finally:
        recipe.save()


if __name__ == '__main__':
    json_file = 'combined_recipies.json'
    with open(json_file, 'r') as f:
        recipies = json.load(f)

    for recipe in recipies:
        process_recipe(recipe)
