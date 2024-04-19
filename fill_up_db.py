import json
import os
import pprint

import django

from orderapp.models import Category, Menu, Product

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_menu.settings')
django.setup()



def process_recipe(recipe):
    category, created = Category.objects.get_or_create(
        title=recipe['category']
    )
    menu, created = Menu.objects.get_or_create(
        title=recipe['menu']
    )
    for ingredient in recipe['ingredients']:
        product, created = Product.objects.get_or_create(
            title=ingredient['title']
        )
        


if __name__ == '__main__':
    json_file = 'combined_recipies.json'
    with open(json_file, 'r') as f:
        recipies = json.load(f)

    pprint.pprint(recipies)
