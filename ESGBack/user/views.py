from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import (
    ActivateEmailSerializer,
    AdminLoginSerializer,
    LoginSerializer,
    LogoutSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    TokenPairResponseSerializer,
    UserProfileSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Registration successful. Please confirm your email."},
            status=status.HTTP_201_CREATED,
        )


class ActivateEmailView(generics.GenericAPIView):
    serializer_class = ActivateEmailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Email confirmed successfully."}, status=status.HTTP_200_OK)

    def get(self, request, token, *args, **kwargs):
        serializer = self.get_serializer(data={"token": token})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Email confirmed successfully."}, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = TokenPairResponseSerializer.build_response(serializer.validated_data["user"])
        return Response(payload, status=status.HTTP_200_OK)


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "If the email exists, a password reset message has been sent."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)

    def get(self, request, token, *args, **kwargs):
        return Response({"token": str(token)}, status=status.HTTP_200_OK)


class AdminLoginView(generics.GenericAPIView):
    serializer_class = AdminLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = TokenPairResponseSerializer.build_response(serializer.validated_data["user"])
        return Response(payload, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
