from django.contrib import admin
from .models import Course, News, Project, Event, Subscriber, Comment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "lang", "isActive", "pars_date")
    list_filter = ("lang", "isActive")
    search_fields = ("title", "site_url")

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "lang", "ar_date", "pars_date")
    list_filter = ("lang",)
    search_fields = ("title", "site_url")

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "lang", "isActive", "pars_date")
    list_filter = ("lang", "isActive")
    search_fields = ("title", "site_url")

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "lang", "event_date", "isActive", "pars_date")
    list_filter = ("lang", "isActive")
    search_fields = ("title", "site_url")

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("email",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "news", "user", "is_approved", "created_at")
    list_filter = ("is_approved",)
    search_fields = ("text", "user__email")
