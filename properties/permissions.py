from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):

    def has_permission(self, request, view):

        if request.method in ['GET']:
            return True

        return (
            request.user.is_authenticated and
            request.user.role == 'OWNER'
        )