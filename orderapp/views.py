import random

from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from orderapp.models import Recipe, Menu, Subscription
from orderapp.payment import create_yoo_payment


def index(request):
    count = Recipe.objects.count()
    random_recipe_id = random.randint(1, count) if count > 0 else None
    context = {
        'random_recipe_id': random_recipe_id,
    }
    return render(request, 'orderapp/index.html', context=context)


def new_order(request):
    context = {
        'vue_data': {
            "date": [
                {"label": "1 мес.", "price": 100},
                {"label": "3 мес.", "price": 250},
                {"label": "6 мес.", "price": 600},
                {"label": "12 мес.", "price": 1000},
            ],
            "menu": [
                {"label": "Завтраки", "price": 100},
                {"label": "Обеды", "price": 200},
                {"label": "Ужины", "price": 300},
                {"label": "Десерты", "price": 400},
            ],
            "quantity": list(range(1, 6)),
            "allergies": [
                {"label": "Рыба и морепродукты", "price": 0},
                {"label": "Зерновые", "price": 0},
                {"label": "Продукты пчеловодства", "price": 0},
                {"label": "Орехи и бобовые", "price": 0},
                {"label": "Молочные продукты", "price": 0},
            ]
        }
    }
    return render(
        request,
        context=context,
        template_name="orderapp/order.html"
    )


def get_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    serialized_recipe = {
        "title": recipe.title,
        "ingredients": [
            {
                ingredient.product.title: ingredient.unit
            } for ingredient in recipe.ingredients.all()
        ],
        "description": recipe.description,
        "calories": recipe.calories,
        "image": recipe.image.url if recipe.image else staticfiles_storage.url("img/circle1.png")
    }
    return render(
        request,
        'orderapp/recipe.html',
        {'recipe': serialized_recipe}
    )


@csrf_exempt
@login_required
def make_payment(request):
    params = request.POST
    duration_mapping = {
        '0': 1,
        '1': 3,
        '2': 6,
        '3': 12,
    }
    menu_mapping = {
        'classic': 'Классическое',
        'low': 'Низкоуглеводное',
        'keto': 'Кето',
        'veg': 'Вегетарианское'
    }
    sub_period = duration_mapping[params.get('period', 0)]
    payment_amount = int(params["cost"])
    payment = create_yoo_payment(payment_amount, 'RUB', sub_period, params)
    menu, created = Menu.objects.get_or_create(title=menu_mapping[params.get('foodtype', 'classic')])
    Subscription.objects.create(
        months=str(sub_period),
        persons=params.get('select_quantity', '1'),
        cost=payment_amount,
        menu=menu,
        breakfast=params.get('select0', "0") == "1",
        lunch=params.get('select1', "0") == "1",
        dinner=params.get('select2', "0") == "1",
        dessert=params.get('select3', "0") == "1",
        user=request.user
    )
    return redirect(payment["confirmation"]["confirmation_url"])
