from django.urls import path
from .views import new_order, make_payment, get_recipe, check_payment


urlpatterns = [
    path('payment/', make_payment, name='payment'),
    path('', new_order, name='order'),
    path('recipies/<int:recipe_id>/', get_recipe, name='get_recipe'),
    path('check_payment/', check_payment, name='check_payment'),

]
