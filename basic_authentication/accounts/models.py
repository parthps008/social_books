from django.contrib.auth.models import AbstractUser
from django.db import models
from django_filters import FilterSet

class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    public_visibility = models.BooleanField(default=False)
    
    @property
    def age(self):
        from datetime import date
        if self.birth_year:
            today = date.today()
            return today.year - self.birth_year
        return None

class UserFilter(FilterSet):
    class Meta:
        model = CustomUser
        fields = ['public_visibility']

class UploadedFile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link the file to a user
    file = models.FileField(upload_to='uploads/')  # Store the file in the 'uploads/' directory
    title = models.CharField(max_length=255)  # Title of the file/book
    description = models.TextField(blank=True)  # Optional description
    visibility = models.BooleanField(default=True)  # Public or private visibility
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Optional cost
    year_of_publication = models.PositiveIntegerField(blank=True, null=True)  # Year of publication (optional)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the file was uploaded

    def __str__(self):
        return self.title
