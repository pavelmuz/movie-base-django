from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsMovieOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user.profile


class IsProfileOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj == request.user.profile


class IsNotificationRecipientOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.recipient == request.user.profile


class IsAuthenticatedOrPatchDeleteOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['PATCH', 'DELETE']:
            return request.user and request.user.is_authenticated
        return True
