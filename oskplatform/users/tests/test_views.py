from django.test import TestCase
from users.models import CustomUser


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_login_view(self):
        response = self.client.post(
            "/login/", {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_login_view_with_wrong_password(self):
        response = self.client.post(
            "/login/", {"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Niepoprawna nazwa użytkownika lub hasło.")

    def test_login_view_with_wrong_username(self):
        response = self.client.post(
            "/login/", {"username": "wronguser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Niepoprawna nazwa użytkownika lub hasło.")

    def test_login_view_with_empty_username(self):
        response = self.client.post(
            "/login/", {"username": "", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Niepoprawna nazwa użytkownika lub hasło.")

    def test_get_login_view(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Zaloguj się")


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_logout_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
