from django.core.validators import RegexValidator
from django.db import models
from ESGBack import settings
from user.models import User
import uuid

class Base(models.Model):
    title = models.TextField(null=True, blank=True)
    pars_date = models.DateTimeField(auto_now_add=True)
    digest = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True, max_length=2000)
    site_url = models.URLField()
    lang = models.CharField(max_length=2, validators=[RegexValidator('en|ru|kk')])

class Course(Base):
    cr_site_url = models.URLField(max_length=2000)
    isActive = models.BooleanField(default=True)
    def __str__(self):
        return self.title

class News(Base):
    ar_date = models.DateTimeField(null=True, blank=True)
    ar_site_url = models.URLField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-ar_date']

class Project(Base):
    pr_site_url = models.URLField(max_length=2000)
    isActive = models.BooleanField(default=True)
    def __str__(self):
        return self.title

class Event(Base):
    ev_site_url = models.URLField(max_length=2000)
    event_date = models.DateTimeField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-event_date']

class Subscriber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="subscription", null=True, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    confirm_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    genre_preferences = models.JSONField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
