from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, StudentProfile, SupervisorProfile


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ("email", "username", "role", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get("role")

        if commit:
            user.save()
            # Create profile based on role
            if role == "student":
                StudentProfile.objects.create(user=user)
            elif role == "supervisor":
                SupervisorProfile.objects.create(user=user)

        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "username", "role")


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["phone", "student_id", "company", "session"]


class SupervisorProfileForm(forms.ModelForm):
    class Meta:
        model = SupervisorProfile
        fields = ["phone", "campus"]
