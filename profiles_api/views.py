from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters

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
    serializer_class = serializers.UserProfileSerialzers
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)
