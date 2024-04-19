import json
import os

import django

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
    meal, created = Meal.objects.get_or_create(
        title=recipe_info['category']
    )
    menu, created = Menu.objects.get_or_create(
        title=recipe_info['menu']
    )
    recipe, created = Recipe.objects.get_or_create(
        title=recipe_info['title'],
        description=recipe_info['description'],
        meal=meal,
        menu=menu
    )
    for ingredient in recipe_info['ingredients']:
        if 'units_amount' in ingredient:
            ingredient['unit'] = ingredient['units_amount']
            del ingredient['units_amount']

        product, created = Product.objects.get_or_create(
            title=ingredient['title']
        )
        if ingredient['intolerance'] in rus_allergies:
            allergy, created = Allergy.objects.get_or_create(
                title=ingredient['intolerance']
            )
            product.allergy = allergy
        else:
            allergy, created = Allergy.objects.get_or_create(
                title='Нет'
            )
            product.allergy = allergy
        product.save()
        print(ingredient)
        Ingredient.objects.get_or_create(
            unit=ingredient['unit'],
            calories=ingredient['calories'],
            product=product,
            recipe=recipe
        )

    ingredients = recipe.ingredients.all()
    calories = sum(ingredient.calories for ingredient in ingredients)
    recipe.calories = calories
    recipe.save()


if __name__ == '__main__':
    json_file = 'combined_recipies.json'
    with open(json_file, 'r') as f:
        recipies = json.load(f)

    for recipe in recipies:
        process_recipe(recipe)
