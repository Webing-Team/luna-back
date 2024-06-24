from django.db import models
from accounts.models import Profile


class Group(models.Model):
    name_group = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    owner_id = models.IntegerField()
    admins = models.ManyToManyField(Profile, related_name='admin_groups', verbose_name='admins')
    users = models.ManyToManyField(Profile, verbose_name=("users"))

    def __str__(self):
        return self.name_group


class GroupPost(models.Model):
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=150)
    user = models.ForeignKey(Profile, related_name='group_post_user', null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(Group, related_name='group_posts', on_delete=models.CASCADE)

    def __str__(self):
        return f'id {self.user_id}'




