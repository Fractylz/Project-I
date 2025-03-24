from django.contrib import admin
from .models import CustomUser, StudentProfile, SupervisorProfile


# Register your models here.
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "student_id", "company", "session"]
    search_fields = ["user__username", "student_id"]


@admin.register(SupervisorProfile)
class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "campus"]
    search_fields = ["user__username", "campus"]
