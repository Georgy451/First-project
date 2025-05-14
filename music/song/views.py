from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import * 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TrackUploadForm, RegisterUserForm, LoginUserForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView



def index(request):
    return render(request, 'song/index.html')

def base(request): 
    return render(request, 'song/base.html')


def user(request):
    return render(request, 'song/user.html')
def track(request):
    songs = Track.objects.filter(user=request.user).all()
    return render(request, 'song/track.html', {'songs': songs,})
    


def install(request):
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
    
    return render(request, 'song/install.html', {'form': form})



def profile(request):
    user_tracks = Track.objects.filter(user=request.user).values('title', 'audio_file')
    tracks_count = user_tracks.count()  
    username = request.user.username
    
    context = {
        'username': username,
        'bio': 'Слушаю и создаю музыку',
        'tracks_count': tracks_count,
        'followers_count': 0,  
        'following_count': 0, 
        'user_tracks': user_tracks,
    }
    return render(request, 'song/profile.html', context)

def about(request):
    return render(request, 'song/about.html')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'song/register.html'  
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Регистрация"
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
    
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'song/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Авторизация"
        return context

    def get_success_url(self):
        return reverse_lazy('base')

def logout_user(request):
    logout(request)
    return redirect('login')







