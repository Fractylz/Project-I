from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import StudentProfile, SupervisorProfile


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get("role")

            # Create the corresponding profile
            if role == "student":
                StudentProfile.objects.create(user=user)
            elif role == "supervisor":
                SupervisorProfile.objects.create(user=user)

            login(request, user)  # Log in the user after registration
            return redirect("home")  # Change to your desired redirect page

    else:
        form = CustomUserCreationForm()

    return render(request, "accounts/register.html", {"form": form})
