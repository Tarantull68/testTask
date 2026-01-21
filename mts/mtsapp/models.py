'''from django.db import models
from django.utils import timezone


class Chat(models.Model):
    title = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')  # если нужен пользователь
    text = models.TextField(null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.text[:50]}..."  # первые 50 символов текста'''

from django.db import models
from django.utils import timezone

class Chat(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название чата")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')  # если нужен пользователь
    text = models.TextField(null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.text[:50]}..."  # первые 50 символов текста

