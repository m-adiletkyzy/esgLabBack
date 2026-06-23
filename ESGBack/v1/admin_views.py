from django.contrib.auth import get_user_model
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from user.serializers import AdminUserSerializer

from .modelFilters import CourseFilter, EventFilter, NewsFilter, ProjectFilter
from .models import Comment, Course, Event, News, Project, Subscriber
from .permissions import IsAdminOnly
from .serializers import (
    AdminCommentSerializer,
    AdminDashboardSerializer,
    AdminSubscriberSerializer,
    CourseSerializer,
    EventSerializer,
    NewsSerializer,
    ProjectSerializer,
)

User = get_user_model()


class AdminDashboardView(generics.GenericAPIView):
    permission_classes = [IsAdminOnly]
    serializer_class = AdminDashboardSerializer

    def get(self, request, *args, **kwargs):
        payload = {
            "users": User.objects.count(),
            "verified_users": User.objects.filter(is_email_verified=True).count(),
            "active_subscribers": Subscriber.objects.filter(is_active=True).count(),
            "news_count": News.objects.count(),
            "comments_count": Comment.objects.count(),
        }
        serializer = self.get_serializer(payload)
        return Response(serializer.data)


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["email", "username", "first_name", "last_name"]
    ordering_fields = ["date_joined", "email", "last_login"]
    lookup_field = "pk"


class AdminSubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.select_related("user").all().order_by("-created_at")
    serializer_class = AdminSubscriberSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["email", "user__email"]
    ordering_fields = ["created_at", "confirmed_at", "email"]
    lookup_field = "pk"


class AdminCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("user", "news").all().order_by("-created_at")
    serializer_class = AdminCommentSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["text", "user__email", "news__title"]
    ordering_fields = ["created_at", "is_approved"]
    lookup_field = "pk"


class AdminCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter
    lookup_field = "pk"


class AdminNewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter
    lookup_field = "pk"


class AdminProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter
    lookup_field = "pk"


class AdminEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter
    lookup_field = "pk"


class AdminContentSourcesView(generics.GenericAPIView):
    permission_classes = [IsAdminOnly]

    def get(self, request, *args, **kwargs):
        payload = {
            "news_sources": list(News.objects.values("site_url").annotate(count=Count("site_url")).order_by("-count")),
            "course_sources": list(Course.objects.values("site_url").annotate(count=Count("site_url")).order_by("-count")),
            "event_sources": list(Event.objects.values("site_url").annotate(count=Count("site_url")).order_by("-count")),
            "project_sources": list(Project.objects.values("site_url").annotate(count=Count("site_url")).order_by("-count")),
        }
        return Response(payload)
