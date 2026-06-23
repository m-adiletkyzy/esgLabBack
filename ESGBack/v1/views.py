from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .modelFilters import *
from .models import *
from .permissions import IsAdminUserRole, IsOwnerOrAdminOrReadOnly
from .serializers import *
from .services import send_subscription_confirmation_email
from .tasks import repeat_order_make, run_all_parsers


news_list_schema = extend_schema(
    summary="List news",
    description=(
        "Supports filters: lang, site_url, title, digest, ar_date_after, ar_date_before. "
        "Also supports search, ordering, limit, offset."
    ),
)

project_list_schema = extend_schema(
    summary="List projects",
    description="Supports filters: lang, site_url, title, digest, isActive, plus search, ordering, limit, offset.",
)

event_list_schema = extend_schema(
    summary="List events",
    description=(
        "Supports filters: lang, site_url, title, digest, isActive, event_date_after, event_date_before. "
        "Also supports search, ordering, limit, offset."
    ),
)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    permission_classes = [IsAdminUserRole]
    lookup_field = "pk"
    search_fields = ["title", "digest", "site_url", "cr_site_url"]
    ordering_fields = ["pars_date", "title", "lang"]
    ordering = ["-pars_date"]


@extend_schema_view(list=news_list_schema)
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NewsFilter
    permission_classes = [IsAdminUserRole]
    lookup_field = "pk"
    search_fields = ["title", "digest", "site_url", "ar_site_url"]
    ordering_fields = ["pars_date", "ar_date", "title", "lang"]
    ordering = ["-ar_date", "-pars_date"]


@extend_schema_view(list=project_list_schema)
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProjectFilter
    permission_classes = [IsAdminUserRole]
    lookup_field = "pk"
    search_fields = ["title", "digest", "site_url", "pr_site_url"]
    ordering_fields = ["pars_date", "title", "lang"]
    ordering = ["-pars_date"]


@extend_schema_view(list=event_list_schema)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = EventFilter
    permission_classes = [IsAdminUserRole]
    lookup_field = "pk"
    search_fields = ["title", "digest", "site_url", "ev_site_url"]
    ordering_fields = ["pars_date", "event_date", "title", "lang"]
    ordering = ["-event_date", "-pars_date"]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]
    lookup_field = "pk"

    def get_queryset(self):
        qs = Comment.objects.all().order_by("-created_at")
        if self.request.user and self.request.user.is_authenticated and (
            self.request.user.is_staff
            or self.request.user.is_superuser
            or getattr(self.request.user, "role", "") == "ADMIN"
        ):
            return qs
        return qs.filter(is_approved=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def getSiteListBase(r, Obj):
    if r.method == "GET":
        sites = Obj.objects.values("site_url").annotate(count=Count("site_url")).order_by("-count")
        return Response(sites)


@api_view(["GET"])
def getNewsSiteList(request):
    return getSiteListBase(request, News)


@api_view(["GET"])
def getCourseSiteList(request):
    return getSiteListBase(request, Course)


@api_view(["GET"])
def getEventSiteList(request):
    return getSiteListBase(request, Event)


@api_view(["GET"])
def getProjectSiteList(request):
    return getSiteListBase(request, Project)


class SubscribeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Subscribe authenticated user",
        description="Uses current authenticated user email, creates/updates subscriber and sends confirmation email.",
        responses={
            201: OpenApiResponse(description="Confirmation email sent"),
            200: OpenApiResponse(description="Already subscribed"),
            400: OpenApiResponse(description="Email missing or invalid"),
            401: OpenApiResponse(description="Authentication required"),
        },
    )
    def post(self, request):
        email = request.user.email

        if not email:
            return Response({"error": "User email is required."}, status=400)

        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "Invalid email."}, status=400)

        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={"user": request.user, "is_active": False},
        )

        if not created and subscriber.is_active:
            return Response({"detail": "Already subscribed."}, status=200)

        if subscriber.user_id is None:
            subscriber.user = request.user
            subscriber.save(update_fields=["user"])

        send_subscription_confirmation_email(request, subscriber)
        return Response({"detail": "Check email to confirm subscription."}, status=201)


class SubscribeConfirmView(APIView):
    def get(self, request, token):
        try:
            subscriber = Subscriber.objects.get(confirm_token=token)
        except Subscriber.DoesNotExist:
            return Response({"error": "Invalid token."}, status=400)

        if subscriber.is_active:
            return Response({"detail": "Subscription already confirmed."}, status=200)

        subscriber.is_active = True
        subscriber.confirmed_at = timezone.now()
        subscriber.save(update_fields=["is_active", "confirmed_at"])
        return Response({"detail": "Subscription confirmed."}, status=200)


class RunParsersView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        remote_addr = self.request.META.get("REMOTE_ADDR")
        if settings.DEBUG and remote_addr in {"127.0.0.1", "::1", "localhost"}:
            return [permissions.AllowAny()]
        return [permission() for permission in self.permission_classes]

    @extend_schema(
        summary="Run all parsers",
        description="Body accepts { mode: 'sync' | 'async' }. Runs parser pipeline and returns status.",
        responses={
            200: OpenApiResponse(description="Parsers finished in sync mode"),
            202: OpenApiResponse(description="Parsers started in async mode"),
            500: OpenApiResponse(description="Parser run failed"),
        },
    )
    def post(self, request):
        mode = request.data.get("mode", "sync")

        if mode == "async":
            try:
                task = repeat_order_make.delay()
                return Response(
                    {
                        "detail": "Parser run started in background.",
                        "mode": "async",
                        "task_id": task.id,
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
            except Exception as exc:
                return Response(
                    {"error": f"Could not start async parser run: {exc}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        try:
            run_all_parsers()
            return Response(
                {
                    "detail": "Parser run completed.",
                    "mode": "sync",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as exc:
            return Response(
                {"error": f"Parser run failed: {exc}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
