from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='home'),
    path('base', base, name='base'),
    path('profile', profile, name='profile'),
    path('about', about, name='about'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('track', track, name='track'),
    path('user', user, name='user'),
    path('install', install, name='install'),
    path('subscribe/<int:user_id>/', subscribe, name='subscribe'),
    path('unsubscribe/<int:user_id>/', unsubscribe, name='unsubscribe'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)