from django.db import models

from accounts.models import User, Profile


class FriendShip(models.Model):
    from_user = models.ForeignKey(Profile, related_name='friend_request_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile, related_name='friend_request_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('from_user', 'to_user'))

    def __str__(self):
        return f'{self.from_user} -> {self.to_user}'