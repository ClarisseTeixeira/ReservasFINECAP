from django.urls import path
from .views import *

urlpatterns = [
    path('accounts/login/', user_login, name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    path('registro/', registro, name='registro'),
    path('', index, name='index')
]

