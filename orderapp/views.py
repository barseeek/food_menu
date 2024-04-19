from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from orderapp.payment import create_yoo_payment


def index(request):
    return render(request, 'orderapp/index.html')


def new_order(request):
    return render(request, "orderapp/order.html")


@csrf_exempt
def make_payment(request):
    payment = create_yoo_payment(100, 'RUB', 1)
    return redirect(payment["confirmation"]["confirmation_url"])