from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


class HelloApiView(APIView):
    """Test Api View"""
    serializer_class = serializers.HelloSerializers
    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_ApiView = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is Similar to traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message':'Hello', 'an_ApiView':an_ApiView})
    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({'method':'PUT'})


    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method':'PATCH'})


    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method':'DELETE'})



class HelloViewSet(viewsets.ViewSet):
    """Test an ViewSet"""
    serializer_class = serializers.HelloSerializers
    def list(self, request):
        """Returns an list of features"""
        an_viewset = [
            'uses action (list, create, retrieve, update, partial_update)',
            'Automatically maps to Urls using Routers',
            'Provides more functionality with less code',
        ]

        return Response({'message':'Hello', 'an_viewset': an_viewset})
    def create(self, request):
        """Create a new hello Message"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'Message':message})
        else:
            return Response(
                  serializer.errors,
                  status=status.HTTP_400_BAD_REQUEST
            )


    def retrieve(self, request, pk=None):
        """Handle getting an object by its Id"""
        return Response({'http_method':'GET'})


    def update(self, request, pk=None):
        """Handle updating an object"""
        return Response({'Http_method': 'PUT'})


    def partial_update(self, request, pk=None):
        """Handle partially updating an object"""
        return Response({'Http_method':'PATCH'})


    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'Http_method':'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializers # This links the UserProfileSerializers class to this view function
    queryset = models.UserProfile.objects.all()  # This manages all the objects of the UserProfile in the ViewSet.
    authentication_classes = (TokenAuthentication,) # This helps in authenticating the requests to our endpoints.
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle Creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializers
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )
    # This perform_create function is an handy function in django rest framework that allows you to override the behaviour for creating the objects through model ModelViewSet.
    def perform_create(self,serializer):
        """Sets the user profile to the logged in user"""

        # Serializer.save is a function that Automatically runs after the data has been validated to save the data in the database and
        # we are customizing it here so that we can set the user user_profile to the current logged in user so that the feed can be saved by user name only.
        serializer.save(user_profile=self.request.user)
