import datetime
import json
import random
from time import sleep

from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from yookassa import Payment

from orderapp.models import Recipe, Menu, Subscription, Allergy
from orderapp.payment import create_yoo_payment


def index(request):
    count = Recipe.objects.count()
    random_recipe_id = random.randint(1, count) if count > 0 else None
    sub_counter = 0
    if request.user.is_authenticated:
        sub_counter = Subscription.objects.filter(user=request.user, end__gt=datetime.datetime.now().date()).count()
    context = {
        'random_recipe_id': random_recipe_id,
        'sub_counter': sub_counter
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

    payment_amount = int(params["cost"])
    try:
        payment = create_yoo_payment(request, payment_amount, 'RUB', params)
    except Exception as e:
        return HttpResponse(f'Возникла ошибка при оплате {e}'.format(e=e))

    return redirect(payment["confirmation"]["confirmation_url"], payment_id=payment["id"])


def create_subscription(payment, subscription_data, user):
    menu_mapping = {
        'classic': 'Классическое',
        'low': 'Низкоуглеводное',
        'keto': 'Кето',
        'veg': 'Вегетарианское'
    }
    allergy_labels = [
        "Рыба и морепродукты", "Зерновые", "Продукты пчеловодства", "Орехи и бобовые", "Молочные продукты"
    ]
    duration_mapping = {
        '0': 1,
        '1': 3,
        '2': 6,
        '3': 12,
    }
    sub_period = duration_mapping[subscription_data.get('period', 0)]
    payment_amount = int(subscription_data["cost"])
    menu, created = Menu.objects.get_or_create(title=menu_mapping[subscription_data.get('foodtype', 'classic')])
    new_subscription = Subscription.objects.create(
        months=str(sub_period),
        persons=subscription_data.get('select_quantity', '1'),
        cost=int(subscription_data.get('cost')),
        menu=menu,
        breakfast=subscription_data.get('select0', "0") == "1",
        lunch=subscription_data.get('select1', "0") == "1",
        dinner=subscription_data.get('select2', "0") == "1",
        dessert=subscription_data.get('select3', "0") == "1",
        user=user
    )

    selected_allergies = []
    for i in range(5):
        if subscription_data.get(f'allergy{i}', '') == 'on':
            selected_allergies.append(allergy_labels[i])
    if selected_allergies:
        allergies = Allergy.objects.filter(title='Нет')
    else:
        allergies = Allergy.objects.filter(title__in=selected_allergies)
    new_subscription.allergies.add(*allergies)

    new_subscription.save()


@csrf_exempt
@login_required
def check_payment(request):
    payment_id = request.session.get("payment_id")
    subscription_data = request.session.get("subscription_data")
    payment = json.loads((Payment.find_one(payment_id)).json())
    # while payment['status'] == 'pending':
    #     payment = json.loads((Payment.find_one(payment_id)).json())
    #     sleep(3)

    if payment['status'] == 'succeeded':
        create_subscription(payment, subscription_data, request.user)
        request.session['payment_data'] = None
        request.session['subscription_data'] = None
        return redirect(reverse('index'))
    else:
        return HttpResponse('Платеж не прошел, попробуйте еще раз')
