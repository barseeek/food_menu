from django.urls import path
from .views import user_login, register_user, account


urlpatterns = [
    path('', account, name='account'),
    path('login/', user_login, name='login'),
    path('register/', register_user, name='register'),
]
