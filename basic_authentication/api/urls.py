from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from djoser.views import TokenCreateView, TokenDestroyView
from .views import UserUploadedFilesView

urlpatterns = [
    # Token management endpoints using Djoser
    path('login/', TokenCreateView.as_view(), name='api_login'),  # Create a new token for login
    path('logout/', TokenDestroyView.as_view(), name='api_logout'),  # Destroy token (logout)

    # Custom endpoint to access user-uploaded files
    path('files/', UserUploadedFilesView.as_view(), name='user_files'),  # List files uploaded by the user
]
