from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):
    """Test Api View"""
    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_ApiView = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is Similar to traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message':'Hello', 'an_ApiView':an_ApiView})
