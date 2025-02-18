from django.contrib import admin

from .models import CustomUser, StudentProfile, SupervisorProfile


class CustomUserAdmin(admin.ModelAdmin):