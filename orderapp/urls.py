from django.urls import path
from .views import new_order, make_payment, get_recipe

urlpatterns = [
    path('payment/', make_payment, name='payment'),
    path('', new_order, name='order'),
    path('recipies/<int:recipe_id>/', get_recipe),
]
