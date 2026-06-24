from rest_framework import serializers

from v1.parsers.NlpMethods import ESG_SUBGENRES, get_esg_subgenres

from .models import Comment, Course, Event, News, Project, Subscriber


class CourseSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, allow_blank=True)
    digest = serializers.CharField(required=True, allow_blank=True)
    image_url = serializers.URLField(required=True, allow_blank=True, allow_null=True)
    site_url = serializers.URLField(required=True)
    lang = serializers.CharField(required=True)
    cr_site_url = serializers.URLField(required=True)

    class Meta:
        model = Course
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = [
            "id",
            "email",
            "is_active",
            "genre_preferences",
            "confirm_token",
            "confirmed_at",
            "created_at",
        ]
        read_only_fields = ["id", "is_active", "confirm_token", "confirmed_at", "created_at"]


class SubscriptionPreferencesSerializer(serializers.Serializer):
    genre_preferences = serializers.ListField(
        child=serializers.ChoiceField(choices=ESG_SUBGENRES),
        allow_empty=True,
    )
    available_genres = serializers.ListField(read_only=True)

    def validate_genre_preferences(self, value):
        return list(dict.fromkeys(value))


class SubscriptionPreferencesReadSerializer(serializers.Serializer):
    genre_preferences = serializers.ListField(
        child=serializers.ChoiceField(choices=ESG_SUBGENRES),
    )
    available_genres = serializers.ListField()
    is_active = serializers.BooleanField()


class AdminSubscriberSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Subscriber
        fields = [
            "id",
            "user",
            "user_email",
            "email",
            "is_active",
            "genre_preferences",
            "confirm_token",
            "confirmed_at",
            "created_at",
        ]
        read_only_fields = ["confirm_token", "confirmed_at", "created_at", "user_email"]


class CommentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "news", "user", "user_email", "text", "is_approved", "created_at"]
        read_only_fields = ["user", "user_email", "is_approved", "created_at"]


class AdminCommentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    news_title = serializers.CharField(source="news.title", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "news", "news_title", "user", "user_email", "text", "is_approved", "created_at"]
        read_only_fields = ["created_at", "user_email", "news_title"]


class AdminDashboardSerializer(serializers.Serializer):
    users = serializers.IntegerField()
    verified_users = serializers.IntegerField()
    active_subscribers = serializers.IntegerField()
    news_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()
