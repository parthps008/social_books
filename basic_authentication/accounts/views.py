from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, CustomUserLoginForm, UploadedFileForm
from .models import UploadedFile
import pandas as pd
import numpy as np 

# Function-based view for user registration
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after signup
            return redirect(reverse_lazy('login'))  # Redirect to the login page
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

# Function-based view for user login
def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Send email notification on successful login
                send_mail(
                    'Login Notification',
                    f'Hello {user.username}, you have successfully logged in.',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = CustomUserLoginForm()

    return render(request, 'login.html', {'form': form})

# Home view displaying users with public_visibility set to True
def home_view(request):
    User = get_user_model()
    users = User.objects.filter(public_visibility=True)
    return render(request, 'home.html', {'users': users})

# View to handle file uploads
@login_required
def upload_books_view(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user  # Assign the current user to the uploaded file
            uploaded_file.save()
            return redirect('uploaded_files')  # Redirect to the uploaded files page
    else:
        form = UploadedFileForm()
    return render(request, 'upload_books.html', {'form': form})

# View to display uploaded files by the current user
@login_required
def uploaded_files_view(request):
    user_files = UploadedFile.objects.filter(user=request.user)

    if not user_files.exists():
        return redirect('upload_books')  # Redirect to Upload Books if no files are found

    # Create a DataFrame from the file data
    data = {
        "Title": [file.title for file in user_files],
        "Cost": [file.cost if file.cost is not None else 0 for file in user_files],
        "Year": [file.year_of_publication if file.year_of_publication is not None else 0 for file in user_files],
    }
    df = pd.DataFrame(data)

    # Apply DataFrame operations
    filtered_df = df[df["Cost"] > 50]
    filtered_df_two_columns = df[(df["Cost"] > 50) & (df["Year"] < 50)]
    replaced_df = df.replace({"Cost": {0: np.nan}})
    dummy_df = pd.DataFrame(np.random.rand(10, 3), columns=["Title", "Cost", "Year"])
    appended_df = pd.concat([df, dummy_df], ignore_index=True)

    # Convert DataFrames to HTML
    df_html = df.to_html()
    filtered_df_html = filtered_df.to_html()
    filtered_df_two_columns_html = filtered_df_two_columns.to_html()
    replaced_df_html = replaced_df.to_html()
    appended_df_html = appended_df.to_html()

    context = {
        'user_files': user_files,
        'df_html': df_html,
        'filtered_df_html': filtered_df_html,
        'filtered_df_two_columns_html': filtered_df_two_columns_html,
        'replaced_df_html': replaced_df_html,
        'appended_df_html': appended_df_html,
    }
    
    return render(request, 'uploaded_files.html', context)

# Custom wrapper for "My Books" dashboard
@login_required
def my_books_view(request):
    user_files = UploadedFile.objects.filter(user=request.user)

    if not user_files.exists():
        return redirect('upload_books')  # Redirect to Upload Books if no files are found

    # Create a DataFrame from the file data
    data = {
        "Title": [file.title for file in user_files],
        "Cost": [file.cost if file.cost is not None else 0 for file in user_files],
        "Year": [file.year_of_publication if file.year_of_publication is not None else 0 for file in user_files],
    }
    df = pd.DataFrame(data)

    # Apply DataFrame operations
    filtered_df = df[df["Cost"] > 50]
    filtered_df_two_columns = df[(df["Cost"] > 50) & (df["Year"] < 50)]
    replaced_df = df.replace({"Cost": {0: np.nan}})
    dummy_df = pd.DataFrame(np.random.rand(10, 3), columns=["Title", "Cost", "Year"])
    appended_df = pd.concat([df, dummy_df], ignore_index=True)

    # Convert DataFrames to HTML
    df_html = df.to_html()
    filtered_df_html = filtered_df.to_html()
    filtered_df_two_columns_html = filtered_df_two_columns.to_html()
    replaced_df_html = replaced_df.to_html()
    appended_df_html = appended_df.to_html()

    context = {
        'user_files': user_files,
        'df_html': df_html,
        'filtered_df_html': filtered_df_html,
        'filtered_df_two_columns_html': filtered_df_two_columns_html,
        'replaced_df_html': replaced_df_html,
        'appended_df_html': appended_df_html,
    }
    
    return render(request, 'my_books.html', context)

# View to delete an uploaded file
@login_required
def delete_file_view(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    uploaded_file.delete()
    return redirect('my_books')

# View to display Authors and Sellers
def authors_and_sellers_view(request):
    User = get_user_model()
    authors_and_sellers = User.objects.filter(public_visibility=True)
    return render(request, 'authors_and_sellers.html', {'authors_and_sellers': authors_and_sellers})
