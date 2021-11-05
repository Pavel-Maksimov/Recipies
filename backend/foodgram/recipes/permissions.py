from rest_framework import permissions


class IsAuthorOrStaff(permissions.BasePermission):
    """
    Permission class for views: recipes.

    Allow access only to staff or instance author.
    Other users are allowed to read data.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author
                or request.user.is_staff)
