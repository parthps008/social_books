from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,UploadedFile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Add any additional configurations or fieldsets here

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'visibility', 'cost', 'year_of_publication', 'uploaded_at')
    list_filter = ('visibility', 'year_of_publication')
    search_fields = ('title', 'description', 'user__username')
