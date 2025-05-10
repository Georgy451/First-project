from django.shortcuts import render, redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import * 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TrackUploadForm

def index(request):
    return render(request,'song/index.html',)

def base(request):
    if request.method == 'POST':
        form = TrackUploadForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            if request.user.is_authenticated: 
                track.user = request.user
            track.save()
            messages.success(request, 'Трек успешно загружен!')
            return redirect('base')
    else:
        form = TrackUploadForm()
    
    return render(request, 'song/base.html', {'form': form})

def profile(request):
  
    user_tracks = Track.objects.values('title', 'artist') 
    tracks_count = user_tracks.count()  
    
    context = {
        'username': 'МузыкальныйЭнтузиаст',
        'bio': 'Слушаю и создаю музыку',
        'tracks_count': tracks_count,
        'followers_count': 0,  
        'following_count': 0, 
        'user_tracks': user_tracks,
    }
    return render(request, 'song/profile.html', context)

def search(request):
    return render(request, 'song/search.html')


def about(request):
    return render(request, 'song/about.html')






