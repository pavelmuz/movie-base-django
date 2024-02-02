from rest_framework import serializers
from users.models import Profile, Follow
from movies.models import Movie, Like, Comment
from chats.models import Message
from notifications.models import Notification


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)

    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)

    class Meta:
        model = Comment
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)

    class Meta:
        model = Movie
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    follower = ProfileSerializer()
    following = ProfileSerializer()

    class Meta:
        model = Follow
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer()
    recipient = ProfileSerializer()

    class Meta:
        model = Message
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    recipient = ProfileSerializer()
    sender = ProfileSerializer()
    movie = MovieSerializer()
    message = MessageSerializer()

    class Meta:
        model = Notification
        fields = '__all__'
