from django import forms
from .models import Track

class TrackUploadForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'artist', 'audio_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Название трека',
                'class': 'form-input'
            }),
            'artist': forms.TextInput(attrs={
                'placeholder': 'Исполнитель',
                'class': 'form-input'
            }),
            'audio_file': forms.FileInput(attrs={
                'accept': 'audio/*',
                'class': 'form-input-file'
            }),
        }