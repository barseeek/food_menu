from django.urls import path
from .views import new_order, make_payment


urlpatterns = [
    path('payment/', make_payment, name='payment'),
    path('', new_order, name='order'),
]
