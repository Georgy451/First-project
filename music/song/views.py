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
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User


def index(request):
    return render(request, 'song/index.html')

def base(request): 
    return render(request, 'song/base.html')

def user(request):
    users = User.objects.all()
    return render(request, 'song/user.html', {'users': users})

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



@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    tracks_count = Track.objects.filter(user=request.user).count()
    followers_count = profile.followers.count()
    following_count = profile.subscriptions.count()

    if request.method == "POST":
        bio = request.POST.get("bio", "")
        profile.bio = bio
        profile.save()

    context = {
        "username": request.user.username,
        "bio": profile.bio,
        "tracks_count": tracks_count,
        "followers_count": followers_count,
        "following_count": following_count,
    }
    return render(request, "song/profile.html", context)

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

@login_required
def subscribe(request, user_id):
    if request.method == "POST":
        user_to_subscribe = get_object_or_404(User, id=user_id)
        profile, _ = Profile.objects.get_or_create(user=request.user)
        target_profile, _ = Profile.objects.get_or_create(user=user_to_subscribe)
        if user_to_subscribe != request.user:
            profile.subscriptions.add(target_profile)
    return redirect(request.META.get('HTTP_REFERER', 'user'))

@login_required
def unsubscribe(request, user_id):
    if request.method == "POST":
        user_to_unsubscribe = get_object_or_404(User, id=user_id)
        profile, _ = Profile.objects.get_or_create(user=request.user)
        target_profile, _ = Profile.objects.get_or_create(user=user_to_unsubscribe)
        if user_to_unsubscribe != request.user:
            profile.subscriptions.remove(target_profile)
    return redirect(request.META.get('HTTP_REFERER', 'user'))







