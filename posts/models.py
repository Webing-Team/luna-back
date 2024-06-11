from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField(max_length=65)
    text = models.CharField(max_length=150)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts'
    )


    def __str__(self):
        # Post by {self.user} -
        return f'id {self.id}'
