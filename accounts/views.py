from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import StudentProfile, SupervisorProfile


class RegistrationFormView(FormView):
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("home")  # Change this to your actual home page

    def form_valid(self, form):
        user = form.save()
        role = form.cleaned_data.get("role")

        # Create the corresponding profile
        if role == "student":
            StudentProfile.objects.create(user=user)
        elif role == "supervisor":
            SupervisorProfile.objects.create(user=user)

        login(self.request, user)  # Log in the user after registration
        return super().form_valid(form)
