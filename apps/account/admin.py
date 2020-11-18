from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'username',]
    list_filter = ['email', 'is_active', 'is_staff', 'date_joined', 'is_superuser']
    list_editable = ['is_active']
