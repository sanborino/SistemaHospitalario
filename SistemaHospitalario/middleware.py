# sistemsahospitalario/middleware.py


class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"
        return response


from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseForbidden


from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from acceso.models import UsuarioRol


class RoleRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            # Verificamos si el usuario tiene roles en tu modelo
            tiene_roles = UsuarioRol.objects.filter(usuario=request.user).exists()

            if not tiene_roles:
                # Permitimos solo Inicio y Salir
                allowed_paths = [
                    reverse("acceso:hospitales"),  # tu vista de inicio
                    reverse("acceso:logout"),  # tu vista de logout
                ]
                if not any(request.path.startswith(path) for path in allowed_paths):
                    # Mostrar página 403 personalizada
                    return HttpResponseForbidden(render(request, "403.html"))
        return self.get_response(request)
