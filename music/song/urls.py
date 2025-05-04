from django.urls import path
from . import views
urlpatterns = [
path('', views.index, name='home'),
path('base', views.base, name='base'),
path('profile', views.profile, name='profile'),
path('about', views.about, name='about'),
path('search', views.search, name='search'),
path('profile', views.profile, name='profile'),


]