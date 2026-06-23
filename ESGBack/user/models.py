import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(unique=True, null=True, blank=True, editable=False)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)
    password_reset_token = models.UUIDField(unique=True, null=True, blank=True, editable=False)
    password_reset_sent_at = models.DateTimeField(null=True, blank=True)

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"
        GUEST = "GUEST", "Guest"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if self.is_staff or self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)

    def issue_email_verification_token(self):
        self.email_verification_token = uuid.uuid4()
        return self.email_verification_token

    def issue_password_reset_token(self):
        self.password_reset_token = uuid.uuid4()
        return self.password_reset_token
