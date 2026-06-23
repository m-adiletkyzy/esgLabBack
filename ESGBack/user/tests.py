from django.core import mail
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class AuthFlowTests(APITestCase):
    def test_register_activate_and_login_flow(self):
        register_payload = {
            "email": "user1@example.com",
            "password": "StrongPass123",
            "re_password": "StrongPass123",
            "first_name": "User",
            "last_name": "One",
        }

        register_response = self.client.post("/api/v1/auth/register/", register_payload, format="json")

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="user1@example.com")
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_email_verified)
        self.assertIsNotNone(user.email_verification_token)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(str(user.email_verification_token), mail.outbox[0].body)

        login_response = self.client.post(
            "/api/v1/auth/login/",
            {"email": "user1@example.com", "password": "StrongPass123"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_401_UNAUTHORIZED)

        activate_response = self.client.post(
            "/api/v1/auth/activate/",
            {"token": str(user.email_verification_token)},
            format="json",
        )
        self.assertEqual(activate_response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_email_verified)
        self.assertIsNone(user.email_verification_token)

        login_response = self.client.post(
            "/api/v1/auth/login/",
            {"email": "user1@example.com", "password": "StrongPass123"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)
        self.assertEqual(login_response.data["user"]["email"], "user1@example.com")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")
        me_response = self.client.get("/api/v1/auth/me/")
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
        self.assertEqual(me_response.data["email"], "user1@example.com")

    def test_admin_login_requires_admin_permissions(self):
        user = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="StrongPass123",
            is_active=True,
            is_email_verified=True,
        )

        response = self.client.post(
            "/api/v1/auth/admin/login/",
            {"email": user.email, "password": "StrongPass123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_password_reset_flow(self):
        user = User.objects.create_user(
            username="user3",
            email="user3@example.com",
            password="StrongPass123",
            is_active=True,
            is_email_verified=True,
        )

        response = self.client.post(
            "/api/v1/auth/password-reset/",
            {"email": user.email},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertIsNotNone(user.password_reset_token)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(str(user.password_reset_token), mail.outbox[0].body)

        confirm_response = self.client.post(
            "/api/v1/auth/password-reset/confirm/",
            {
                "token": str(user.password_reset_token),
                "password": "NewStrongPass123",
                "re_password": "NewStrongPass123",
            },
            format="json",
        )
        self.assertEqual(confirm_response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertIsNone(user.password_reset_token)
        self.assertTrue(user.check_password("NewStrongPass123"))

        login_response = self.client.post(
            "/api/v1/auth/login/",
            {"email": user.email, "password": "NewStrongPass123"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

    def test_password_reset_request_is_safe_for_unknown_email(self):
        response = self.client.post(
            "/api/v1/auth/password-reset/",
            {"email": "missing@example.com"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 0)
