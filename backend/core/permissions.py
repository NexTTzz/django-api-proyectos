from rest_framework.permissions import BasePermission

class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

class SoloLecturaCliente(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.method in ['GET']
