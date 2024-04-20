from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from orderapp.payment import create_yoo_payment


def index(request):
    return render(request, 'orderapp/index.html')


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
            "quantity": list(range(1, 7)),
            "allergies": [
                {"label": "Рыба и морепродукты", "price": 0},
                {"label": "Мясо", "price": 0},
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


@csrf_exempt
def make_payment(request):
    payment = create_yoo_payment(100, 'RUB', 1)
    return redirect(payment["confirmation"]["confirmation_url"])
