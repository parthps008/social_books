from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UploadedFileSerializer
from accounts.models import UploadedFile

class CustomTokenCreateView(APIView):
    """
    API endpoint to obtain an authentication token.
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)

class UserUploadedFilesView(APIView):
    """
    API endpoint to get files uploaded by the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        user_files = UploadedFile.objects.filter(user=user)
        serializer = UploadedFileSerializer(user_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
