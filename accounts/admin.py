from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile, SupervisorProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm


class StudentProfileInline(admin.StackedInline):
    """Inline admin for StudentProfile, shown in CustomUserAdmin when role is 'student'."""

    model = StudentProfile
    can_delete = False
    extra = 0


class SupervisorProfileInline(admin.StackedInline):
    """Inline admin for SupervisorProfile, shown in CustomUserAdmin when role is 'supervisor'."""

    model = SupervisorProfile
    can_delete = False
    extra = 0


class CustomUserAdmin(UserAdmin):
    """Custom admin panel for CustomUser."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("email", "username", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "username", "password", "role")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "role",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    search_fields = ("email", "username")
    ordering = ("email",)

    def save_model(self, request, obj, form, change):
        """Ensure user profile is created when a user is added via the admin panel."""
        super().save_model(request, obj, form, change)
        if not change:  # Only create profile for new users
            if obj.role == "student" and not hasattr(obj, "studentprofile"):
                StudentProfile.objects.create(user=obj)
            elif obj.role == "supervisor" and not hasattr(obj, "supervisorprofile"):
                SupervisorProfile.objects.create(user=obj)

    def get_inline_instances(self, request, obj=None):
        """Dynamically show the correct profile inline based on user role."""
        if obj:  # Editing an existing user
            if obj.role == "student":
                return [StudentProfileInline(self.model, self.admin_site)]
            elif obj.role == "supervisor":
                return [SupervisorProfileInline(self.model, self.admin_site)]
        return []  # No profile inline for new users


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Admin panel for managing Student Profiles separately."""

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    search_fields = ("user__username", "student_id")
    list_filter = ("company", "session")


@admin.register(SupervisorProfile)
class SupervisorProfileAdmin(admin.ModelAdmin):
    """Admin panel for managing Supervisor Profiles separately."""

    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    search_fields = ("user__username", "campus")


admin.site.register(CustomUser, CustomUserAdmin)
