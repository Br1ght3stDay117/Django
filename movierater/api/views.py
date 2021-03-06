from django.http import HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import *


def api_redirect(request):
    return HttpResponseRedirect("/api")


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    authentication_clases = (TokenAuthentication, SessionAuthentication)
    permission_clases = (IsAuthenticated,)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    # authentication_clases=(TokenAuthentication,SessionAuthentication)
    # permission_clases=(IsAuthenticated,)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_clases = (TokenAuthentication, SessionAuthentication)
    permission_clases = (IsAuthenticated,)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_clases = (TokenAuthentication, SessionAuthentication)
    permission_clases = (IsAuthenticated,)

    # @list_route(methods=['post'])
    @action(detail=False, methods=['post'])
    def rate_movie(self, request):
        if 'movie' in request.data and 'user' in request.data and 'stars' in request.data:
            movie = Movie.objects.get(id=request.data['movie'])
            user = User.objects.get(id=request.data['user'])
            stars = request.data['stars']
            try:
                my_rating = Rating.objects.get(movie=movie.id, user=user.id)
                my_rating.stars = stars
                my_rating.save()
                serializer = MovieSerializer(movie, many=False)
                response = {'Message': 'Rating updated', 'Result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                Rating.objects.create(movie=movie, user=user, stars=stars)
                serializer = MovieSerializer(movie, many=False)
                response = {'Message': 'Rating created', 'Result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'Message': 'You need to pass all params'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)
        serializer = UserSerializer(user, many=False)
        return Response({'token': token.key, 'user': serializer.data})
