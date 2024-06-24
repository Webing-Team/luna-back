from rest_framework import serializers

from .models import GroupPost, Group


class CreateGroupSerializer(serializers.ModelSerializer):
    """ Create group
    """

    class Meta:
        model = Group
        fields = ['name_group', 'description', 'owner_id']


class CreateGroupPostSerializer(serializers.ModelSerializer):
    """ Create post
    """
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = GroupPost
        fields = ['user', 'title', 'text']


class JoinGroupSerializer(serializers.ModelSerializer):
    """ Join group
    """

    class Meta:
        model = Group
        fields = ['id']