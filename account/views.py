from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse

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
    return render(
        request=request,
        context={
            "user": request.user,
        },
        template_name='account/lk.html'
    )
