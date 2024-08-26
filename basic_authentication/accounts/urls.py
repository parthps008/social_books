from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    signup_view,
    login_view,
    home_view,
    upload_books_view,
    uploaded_files_view,
    my_books_view,
    delete_file_view,
    authors_and_sellers_view,  # Import the new view
)

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', home_view, name='home'),
    path('upload_books/', upload_books_view, name='upload_books'),
    path('uploaded_files/', uploaded_files_view, name='uploaded_files'),
    path('my_books/', my_books_view, name='my_books'),
    path('delete_file/<int:file_id>/', delete_file_view, name='delete_file'),
    path('authors_and_sellers/', authors_and_sellers_view, name='authors_and_sellers'),  # Add the new URL pattern
]
