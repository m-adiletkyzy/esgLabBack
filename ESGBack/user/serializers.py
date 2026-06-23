from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .services import send_password_reset_email, send_verification_email

User = get_user_model()


def generate_username_from_email(email):
    base_username = email.split("@", 1)[0][:120] or "user"
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username[:110]}-{counter}"
        counter += 1
    return username


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "country",
            "city",
            "avatar",
            "role",
            "is_email_verified",
        ]
        read_only_fields = ["role", "email", "is_email_verified"]


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "country",
            "city",
            "avatar",
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
            "is_email_verified",
            "date_joined",
            "last_login",
        ]
        read_only_fields = ["date_joined", "last_login"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    re_password = serializers.CharField(write_only=True, min_length=8)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "re_password", "first_name", "last_name"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def validate(self, attrs):
        if attrs["password"] != attrs["re_password"]:
            raise serializers.ValidationError({"re_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        validated_data.pop("re_password")
        username = validated_data.pop("username", "").strip()
        email = validated_data.pop("email")
        if not username:
            username = generate_username_from_email(email)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data.pop("password"),
            is_active=False,
            is_email_verified=False,
            **validated_data,
        )
        send_verification_email(request, user)
        return user


class ActivateEmailSerializer(serializers.Serializer):
    token = serializers.UUIDField()

    def validate_token(self, value):
        try:
            self.user = User.objects.get(email_verification_token=value)
        except User.DoesNotExist as exc:
            raise serializers.ValidationError("Invalid or expired verification token.") from exc
        return value

    def save(self, **kwargs):
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.email_verification_token = None
        self.user.save(update_fields=["is_active", "is_email_verified", "email_verification_token"])
        return self.user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"].lower()
        password = attrs["password"]

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist as exc:
            raise AuthenticationFailed("Invalid email or password.") from exc

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid email or password.")
        if not user.is_active:
            raise AuthenticationFailed("Email is not confirmed yet.")

        attrs["user"] = user
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        self.user = User.objects.filter(email__iexact=value.lower()).first()
        return value.lower()

    def save(self, **kwargs):
        request = self.context["request"]
        if self.user and self.user.is_active:
            send_password_reset_email(request, self.user)


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    password = serializers.CharField(write_only=True, min_length=8)
    re_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs["password"] != attrs["re_password"]:
            raise serializers.ValidationError({"re_password": "Passwords do not match."})

        try:
            self.user = User.objects.get(password_reset_token=attrs["token"])
        except User.DoesNotExist as exc:
            raise serializers.ValidationError({"token": "Invalid or expired reset token."}) from exc
        return attrs

    def save(self, **kwargs):
        self.user.set_password(self.validated_data["password"])
        self.user.password_reset_token = None
        self.user.save(update_fields=["password", "password_reset_token"])
        return self.user


class AdminLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = attrs["user"]
        if not (user.is_staff or user.is_superuser or getattr(user, "role", "") == User.Role.ADMIN):
            raise AuthenticationFailed("Admin access is required.")
        return attrs


class TokenPairResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    user = UserProfileSerializer(read_only=True)

    @staticmethod
    def build_response(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserProfileSerializer(user).data,
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.refresh_token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        from rest_framework_simplejwt.exceptions import TokenError

        try:
            token = RefreshToken(self.refresh_token)
            token.blacklist()
        except TokenError:
            return
