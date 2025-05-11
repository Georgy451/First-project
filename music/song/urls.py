from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('base', base, name='base'),
    path('profile', profile, name='profile'),
    path('about', about, name='about'),
    path('search', search, name='search'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
]