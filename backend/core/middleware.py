"""
Middleware personalizado para deshabilitar CSRF en las rutas de API REST
"""
from django.utils.deprecation import MiddlewareMixin


class DisableCSRFForAPI(MiddlewareMixin):
    """
    Middleware que deshabilita la verificación CSRF para todas las rutas que comienzan con /api/
    Esto es seguro porque las APIs REST usan autenticación por tokens en lugar de cookies.
    """
    
    def process_request(self, request):
        # Deshabilitar CSRF para todas las rutas de API
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return None

