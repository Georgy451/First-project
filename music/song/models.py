from django.db import models
from django.contrib.auth.models import User

class Track(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, verbose_name="Название трека")
    audio_file = models.FileField(upload_to='tracks/', verbose_name="Аудиофайл") 
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Аноним'} - {self.title}" 