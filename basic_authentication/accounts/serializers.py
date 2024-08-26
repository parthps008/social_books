from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import UploadedFile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'age', 'birth_year', 'address', 'public_visibility')

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'