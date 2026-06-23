from rest_framework import permissions


class IsAdminUserRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.is_superuser
                or getattr(request.user, "role", "") == "ADMIN"
            )
        )


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_staff
                or request.user.is_superuser
                or getattr(request.user, "role", "") == "ADMIN"
            )
        )


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            if (
                request.user.is_staff
                or request.user.is_superuser
                or getattr(request.user, "role", "") == "ADMIN"
            ):
                return True
            return getattr(obj, "user_id", None) == request.user.id
        return False
