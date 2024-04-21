from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse

from orderapp.models import CustomUser, Subscription, Recipe, Product


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('exampleInputEmail1')
        password = request.POST.get('exampleInputPassword1')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None
        else:
            if not user.check_password(password):
                return HttpResponse('Invalid email')
            login(
                request=request,
                user=user,
            )
            return HttpResponseRedirect(reverse('index'))
    return render(
        request=request,
        template_name='account/login.html',
    )


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


def register_user(request):
    if request.method == 'POST':
        name = request.POST.get('exampleInputName')
        email = request.POST.get('exampleInputEmail')
        password = request.POST.get('exampleInputPassword')
        second_password = request.POST.get('exampleInputSecondPassword')
        if not second_password == password:
            return HttpResponse('Пароли не совпадают')
        user = CustomUser.objects.filter(email=email)
        if user:
            return HttpResponse('You have already created account')
        user = CustomUser.objects.create(
            first_name=name,
            email=email,
            username=email,
        )
        user.set_password(password)
        user.save(update_fields=['password'])
        return HttpResponseRedirect(reverse('index'))
    return render(
        request=request,
        template_name='account/registration.html',
    )


def account(request):
    try:
        subscription = Subscription.objects.get(user=request.user)
    except (Subscription.DoesNotExist, Subscription.MultipleObjectsReturned):
        subscription = None
        return render(
            request=request,
            template_name='orderapp/index.html'
        )
    count_meals = (int(subscription.breakfast) + int(subscription.lunch) +
                   int(subscription.dinner) + int(subscription.dessert))


    # Получаем список аллергий пользователя
    user_allergies = subscription.allergies.all()

    # Создаём список ID продуктов, которые вызывают аллергии
    allergenic_product_ids = Product.objects.filter(allergy__in=user_allergies).values_list('id', flat=True)

    # Фильтруем рецепты, исключая те, что содержат аллергенные продукты
    recipes = Recipe.objects.filter(menu=subscription.menu).exclude(ingredients__product__id__in=allergenic_product_ids).distinct()
    meal_data = {}
    if subscription:
        if subscription.breakfast:
            meal_data['Завтраки'] = recipes.filter(meal__title='Завтраки')
        if subscription.lunch:
            meal_data['Обеды'] = recipes.filter(meal__title='Обеды')
        if subscription.dinner:
            meal_data['Ужины'] = recipes.filter(meal__title='Ужины')
        if subscription.dessert:
            meal_data['Десерты'] = recipes.filter(meal__title='Десерты')

    return render(
        request=request,
        context={
            "user": request.user,
            "subscription": subscription,
            "count_meals": count_meals,
            "meal_data": meal_data
        },
        template_name='account/lk.html'
    )
