from rest_framework import serializers
from users.models import Profile, Follow
from movies.models import Movie, Like, Comment
from chats.models import Message
from notifications.models import Notification


class ProfileShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'name',
            'username',
            'profile_image',
        ]


class FollowerSerializer(serializers.ModelSerializer):
    follower = ProfileShortSerializer()

    class Meta:
        model = Follow
        fields = [
            'follower'
        ]


class FollowingSerializer(serializers.ModelSerializer):
    following = ProfileShortSerializer()

    class Meta:
        model = Follow
        fields = [
            'following'
        ]


class ProfileSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'name',
            'username',
            'email',
            'birthday',
            'profile_image',
            'followers',
            'followings'
        ]

    def get_followers(self, obj):
        followers = Follow.objects.filter(following=obj)
        return FollowerSerializer(instance=followers, many=True).data

    def get_followings(self, obj):
        followings = Follow.objects.filter(follower=obj)
        return FollowingSerializer(instance=followings, many=True).data


class LikeSerializer(serializers.ModelSerializer):
    owner = ProfileShortSerializer(many=False)

    class Meta:
        model = Like
        fields = ['id', 'owner']


class CommentSerializer(serializers.ModelSerializer):
    owner = ProfileShortSerializer(many=False)

    class Meta:
        model = Comment
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    owner = ProfileShortSerializer(many=False)
    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)

    class Meta:
        model = Movie
        fields = [
            'id',
            'owner',
            'title',
            'user_rating',
            'user_review',
            'description',
            'poster_url',
            'created',
            'kinopoisk_url',
            'likes',
            'comments'
        ]


class MovieShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id',
            'title'
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = ProfileShortSerializer()
    recipient = ProfileShortSerializer()

    class Meta:
        model = Message
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    recipient = ProfileShortSerializer()
    sender = ProfileShortSerializer()
    movie = MovieShortSerializer()
    message = MessageSerializer()

    class Meta:
        model = Notification
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    follower = ProfileShortSerializer()
    following = ProfileShortSerializer()

    class Meta:
        model = Follow
        fields = '__all__'
