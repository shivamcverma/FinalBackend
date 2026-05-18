from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated and
            request.user.role == 'OWNER'
        )


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        # Read permissions for everyone
        if request.method in SAFE_METHODS:
            return True

        # Write permissions only to owner
        return obj.owner == request.user

    def has_permission(self, request, view):

        # GET allowed for everyone
        if request.method in SAFE_METHODS:
            return True

        # POST/PUT/DELETE only authenticated OWNER
        return (
            request.user.is_authenticated and
            request.user.role == 'OWNER'
        )