from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from .models import * 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TrackUploadForm, RegisterUserForm, LoginUserForm, ProfileAvatarForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator



def index(request):
    return render(request, 'song/index.html')

@login_required(login_url='/login/') 
def base(request):
    all_tracks = Track.objects.filter(user=request.user)
    all_playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'song/base.html', {
        'all_tracks': all_tracks,
        'all_playlists': all_playlists,
    })

def user(request):
    search_query = request.GET.get('search', '').strip()
    if search_query:
        users = User.objects.filter(username__icontains=search_query)
    else:
        users = User.objects.all()
    return render(request, 'song/user.html', {'users': users})

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, _ = Profile.objects.get_or_create(user=user)
    tracks = Track.objects.filter(user=user)
    followers_count = profile.followers.count()
    following_count = profile.subscriptions.count()
    context = {
        "profile_user": user,
        "bio": profile.bio,
        "status": profile.status,
        "tracks": tracks,
        "tracks_count": tracks.count(),
        "followers_count": followers_count,
        "following_count": following_count,
    }
    return render(request, "song/user_profile.html", context)

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class TrackView(View):
    template_name = 'song/track.html'

    def get(self, request):
        form = TrackUploadForm()
        return self.render_page(request, form)

    def post(self, request):
        if 'add_playlist' in request.POST:
            return self.handle_add_playlist(request)

        if 'add_to_playlist' in request.POST:
            return self.handle_add_to_playlist(request)

        if 'delete_playlist' in request.POST:
            return self.handle_delete_playlist(request)

        if 'delete_track' in request.POST:
            return self.handle_delete_track(request)

        return self.handle_upload_track(request)

    def render_page(self, request, form):
        songs = Track.objects.filter(user=request.user)
        playlists = Playlist.objects.filter(user=request.user)
        return render(request, self.template_name, {
            'songs': songs,
            'form': form,
            'playlists': playlists,
        })

    def handle_add_playlist(self, request):
        name = request.POST.get('playlist_name', '').strip()
        if name:
            Playlist.objects.create(user=request.user, name=name)
            messages.success(request, 'Плейлист создан!')
        return redirect('track')

    def handle_add_to_playlist(self, request):
        track_id = request.POST.get('track_id')
        playlist_id = request.POST.get('playlist_id')
        try:
            playlist = Playlist.objects.get(id=playlist_id, user=request.user)
            track = Track.objects.get(id=track_id, user=request.user)
            playlist.tracks.add(track)
            messages.success(request, 'Трек добавлен в плейлист!')
        except (Playlist.DoesNotExist, Track.DoesNotExist):
            messages.error(request, 'Ошибка при добавлении трека.')
        return redirect('track')

    def handle_delete_playlist(self, request):
        playlist_id = request.POST.get('delete_playlist_id')
        try:
            playlist = Playlist.objects.get(id=playlist_id, user=request.user)
            playlist.delete()
            messages.success(request, 'Плейлист удалён!')
        except Playlist.DoesNotExist:
            messages.error(request, 'Плейлист не найден.')
        return redirect('track')

    def handle_delete_track(self, request):
        track_id = request.POST.get('delete_track_id')
        try:
            track = Track.objects.get(id=track_id, user=request.user)
            track.delete()
            messages.success(request, 'Трек удалён!')
        except Track.DoesNotExist:
            messages.error(request, 'Трек не найден.')
        return redirect('track')

    def handle_upload_track(self, request):
        form = TrackUploadForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.user = request.user
            track.save()
            messages.success(request, 'Трек успешно загружен!')
            return redirect('track')
        else:
            messages.error(request, 'Ошибка загрузки трека.')
        return self.render_page(request, form)


@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    tracks_count = Track.objects.filter(user=request.user).count()
    followers_count = profile.followers.count()
    following_count = profile.subscriptions.count()

    avatar_form = ProfileAvatarForm(instance=profile)
    avatar_url = profile.avatar.url if profile.avatar else None

    if request.method == "POST":
        if "set_status" in request.POST:
            status = request.POST.get("status", "")
            profile.status = status
            profile.save()
        elif "set_avatar" in request.POST:
            avatar_form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
            if avatar_form.is_valid():
                avatar_form.save()
                avatar_url = profile.avatar.url if profile.avatar else None
        else:
            bio = request.POST.get("bio", "")
            profile.bio = bio
            profile.save()

    context = {
        "username": request.user.username,
        "bio": profile.bio,
        "status": profile.status,
        "tracks_count": tracks_count,
        "followers_count": followers_count,
        "following_count": following_count,
        "avatar_form": avatar_form,
        "avatar_url": avatar_url,
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







