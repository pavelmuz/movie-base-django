from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import Profile
from movies.models import Movie
from .serializers import ProfileSerializer, MovieSerializer


@api_view(['GET'])
def get_routes(request):
    routes = [
        {'GET': 'api/profiles'},
        {'GET': 'api/feed'}
    ]
    return Response(routes)


@api_view(['GET'])
def get_profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_feed(request):
    feed = Movie.objects.all()
    serializer = MovieSerializer(feed, many=True)
    return Response(serializer.data)
