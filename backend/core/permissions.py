from rest_framework.permissions import BasePermission


class EsAdmin(BasePermission):
    """
    Permiso para Administradores.
    Los administradores tienen acceso completo (CRUD) a todos los recursos.
    """
    def has_permission(self, request, view):
        """Solo los usuarios staff (administradores) tienen permiso"""
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        """Los administradores pueden acceder a cualquier objeto"""
        return request.user and request.user.is_staff


class SoloLecturaCliente(BasePermission):
    """
    Permiso para Clientes.
    Los clientes solo tienen acceso de lectura (GET, HEAD, OPTIONS).
    Los administradores tienen acceso completo.
    """
    def has_permission(self, request, view):
        """
        Permitir acceso si:
        - Es administrador (acceso completo)
        - Es cliente y método es de solo lectura (GET, HEAD, OPTIONS)
        """
        if request.user and request.user.is_staff:
            return True
        
        # Métodos seguros solo para clientes autenticados
        return request.method in ['GET', 'HEAD', 'OPTIONS']

    def has_object_permission(self, request, view, obj):
        """
        Permitir acceso a nivel de objeto si:
        - Es administrador
        - Es cliente y método es de solo lectura
        """
        if request.user and request.user.is_staff:
            return True
        
        return request.method in ['GET', 'HEAD', 'OPTIONS']