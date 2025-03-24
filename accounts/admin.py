from django.contrib import admin
from .models import CustomUser, StudentProfile, SupervisorProfile


# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "is_staff", "is_superuser"]
    search_fields = ["username", "email"]
    list_filter = ["is_staff", "is_superuser"]


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "student_id", "company", "session"]
    search_fields = ["user__username", "student_id"]


@admin.register(SupervisorProfile)
class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "campus"]
    search_fields = ["user__username", "campus"]


###########33##
