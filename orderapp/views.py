from django.shortcuts import render


def home(request):
    return render(request, template_name='index.html')


def order(request):
    return render(request, template_name='order.html')
