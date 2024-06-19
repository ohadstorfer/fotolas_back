from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
from .models import  CustomUser, Img 

# class CustomUserAdmin(BaseUserAdmin):
#     model = CustomUser
#     list_display = ['email', 'country', 'fullName', 'is_active', 'is_staff']
#     ordering = ['email']  # You can adjust the ordering based on your preference

# Register the CustomUser model with the admin panel
admin.site.register([Img ])
admin.site.register([CustomUser, models.Photographer, models.Spot , models.SessionAlbum , models.Wave ])

