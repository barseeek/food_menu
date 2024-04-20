from django.shortcuts import render
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.models import User

from orderapp.models import CustomUser


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
            return HttpResponse('Authenticate successfully')
    return render(
        request=request,
        template_name='account/login.html',
    )


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
        return HttpResponse('Created successfully')
    return render(
        request=request,
        template_name='account/registration.html',
    )


def account(request):
    return render(
        request=request,
        context={
            "user": request.user,
        },
        template_name='account/lk.html'
    )
