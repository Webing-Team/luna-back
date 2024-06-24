from django.db import models
from accounts.models import User

# Create your models here.
class Chat(models.Model):
    current_users = models.ManyToManyField(User, related_name="chats", blank=True)

    def __str__(self):
        return f"Chat({self.name})"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages", default='')
    text = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message({self.user} {self.chat})"