from django.contrib import admin
from django.conf import settings

from .models import Website


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['title']
