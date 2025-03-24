from django.contrib.auth import get_user_model
from django.test import TestCase


class TestCustomUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()

    def test_create_user(self):
        print("Existing users before test:", list(self.User.objects.all()))

        user = self.User.objects.create_user(
            username="normaluser", email="normal@user.com", password="foo"
        )

        print("User created:", user)

        self.assertEqual(user.username, "normaluser")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # Invalid cases
        with self.assertRaises(TypeError):
            self.User.objects.create_user()

        with self.assertRaises(ValueError):
            self.User.objects.create_user(username="", email="", password="foo")

        with self.assertRaises(ValueError):
            self.User.objects.create_user(
                username="anotheruser", email="", password="foo"
            )  # Changed username

    def test_create_superuser(self):
        admin_user = self.User.objects.create_superuser(
            username="adminuser", email="super@user.com", password="foo"
        )

        self.assertEqual(admin_user.username, "adminuser")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        # Ensure creating a superuser with `is_superuser=False` raises ValueError
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                username="fakeadmin",
                email="fake@user.com",
                password="foo",
                is_superuser=False,
            )
