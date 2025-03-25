from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .managers import CustomUserManager  # Import the custom manager


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("supervisor", "Supervisor"),
    ]
    email = models.EmailField(
        unique=True, blank=False, null=False
    )  # Ensure email is required
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    groups = models.ManyToManyField(
        Group, related_name="customuser_set", blank=True
    )  # Already built in, consider removing
    user_permissions = models.ManyToManyField(
        Permission, related_name="customuser_permissions_set", blank=True
    )
    objects = CustomUserManager()  # Assign the custom manager


class BaseProfile(models.Model):  # Study balik
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    class Meta:
        abstract = True  # Makes it an abstract base class


class StudentProfile(BaseProfile):
    # Native
    student_id = models.CharField(max_length=20, unique=True)
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )
    session = models.ForeignKey(
        "intern_sessions.Session",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )

    # BLI Start of Internship

    # Borang Jawapan Industri
    bli02 = models.FileField(upload_to="bli02/", null=True, blank=True)
    # Surat Perjanjian Latihan Industri
    bli03 = models.FileField(upload_to="bli03/", null=True, blank=True)
    # Borang Akuan Lapor Diri Untuk Latihan Industri di Organisasi
    bli04 = models.FileField(upload_to="bli04/", null=True, blank=True)

    # BLI End of Internship

    # Borang Penialainan Penyelia Akademik
    bli08 = models.FileField(upload_to="bli08/", null=True, blank=True)
    # Borang Penilaian Penyelia Industri
    bli09 = models.FileField(upload_to="bli09/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.student_id})"


class SupervisorProfile(BaseProfile):
    campus = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


# asdsadasdad
