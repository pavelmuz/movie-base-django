from rest_framework import serializers
from users.models import Profile
from movies.models import Movie


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)

    class Meta:
        model = Movie
        fields = '__all__'
