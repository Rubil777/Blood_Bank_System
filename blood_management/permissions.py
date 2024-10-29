from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to allow only admin (staff) users to manage donors and inventory.
    """
    def has_permission(self, request, view):
        # Only allows access if the user is authenticated and is marked as staff (admin)
        return request.user and request.user.is_staff


class IsRegularUser(permissions.BasePermission):
    """
    Custom permission to allow only regular (non-staff) users to request blood.
    """
    def has_permission(self, request, view):
        # Only allows access if the user is authenticated and is NOT staff (admin)
        return request.user and not request.user.is_staff
