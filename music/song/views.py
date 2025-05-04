from django.shortcuts import render
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import * 

def index(request):
    return render(request,'song/index.html',)

def base(request):
    return render(request,'song/base.html',)

def profile(request):
    context = {
        'username': 'МузыкальныйЭнтузиаст',
        'bio': 'Слушаю и создаю музыку',
        'tracks_count': 3,
        'followers_count': 42,
        'following_count': 13,
        'user_tracks': [
            {'title': 'Мой первый трек', 'artist': 'Я', 'plays': 100},
            {'title': 'Летний бит', 'artist': 'Я', 'plays': 75},
            {'title': 'Осенняя мелодия', 'artist': 'Я', 'plays': 50},
        ]
    }
    return render(request, 'song/profile.html', context)

def search(request):
    return render(request, 'song/search.html')


def about(request):
    return render(request, 'song/about.html')






