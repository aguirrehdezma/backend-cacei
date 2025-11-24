from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    # Permiso para usuarios con rol de administrador
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class IsCoordinadorOrAdmin(permissions.BasePermission):
    """
    Permiso para coordinadores y administradores   
    Útil para endpoints de gestión general
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'coordinador']

class IsDocenteOwner(permissions.BasePermission):
    """
    Permiso para que docentes solo accedan a sus propios datos
    Admin y Coordinador pueden acceder a todo
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admin y Coordinador tienen acceso total
        if request.user.role in ['admin', 'coordinador']:
            return True
        
        # Docente solo puede acceder a sus propios datos
        if request.user.is_docente:
            # Verificar si el objeto tiene relación con el profesor del usuario
            if hasattr(obj, 'profesor'):
                return obj.profesor.user == request.user
            # Si el objeto ES el profesor
            if hasattr(obj, 'user'):
                return obj.user == request.user
        
        return False

class ReadOnly(permissions.BasePermission):
    # Permiso de solo lectura para cualquier usuario autenticado
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in permissions.SAFE_METHODS

class IsDocenteOrReadOnly(permissions.BasePermission):
    """
    Los docentes pueden leer todo pero solo modificar sus datos
    Admin y Coordinador pueden todo
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Lectura permitida para todos
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Admin y Coordinador pueden modificar todo
        if request.user.role in ['admin', 'coordinador']:
            return True
        
        # Docente solo puede modificar sus propios datos
        if request.user.is_docente:
            if hasattr(obj, 'profesor'):
                return obj.profesor.user == request.user
            if hasattr(obj, 'user'):
                return obj.user == request.user
        
        return False
