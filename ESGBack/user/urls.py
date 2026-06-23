from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ActivateEmailView,
    AdminLoginView,
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
    UserProfileView,
)

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('activate/', ActivateEmailView.as_view(), name='auth-activate'),
    path('activate/<uuid:token>/', ActivateEmailView.as_view(), name='auth-activate-link'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='auth-password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='auth-password-reset-confirm'),
    path('password-reset/confirm/<uuid:token>/', PasswordResetConfirmView.as_view(), name='auth-password-reset-confirm-link'),
    path('refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('admin/login/', AdminLoginView.as_view(), name='auth-admin-login'),
    path('me/', UserProfileView.as_view(), name='auth-me'),
]
