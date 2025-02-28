from rest_framework.permissions import BasePermission

class esAdmin(BasePermission):
    def tienePermiso(self, request, view):
        if request.user.is_authenticated:
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                return request.user.is_vendedor() or request.user.is_admin()
            return request.user.is_admin()
        return False
    
