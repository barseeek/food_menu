from django.urls import path
from .views import user_login, register_user, account, user_logout

urlpatterns = [
    path('', account, name='account'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register_user, name='register'),
]
