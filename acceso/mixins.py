# acceso/permisos.py
from django.contrib.auth.decorators import user_passes_test
from acceso.models import UsuarioRol
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test


class PermisoAltoMixin(UserPassesTestMixin):
    """
    Mixin para restringir acceso a usuarios con permisos altos:
    - Superuser
    - Rol DIRECCIÓN
    - Rol SISTEMAS
    """

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return UsuarioRol.objects.filter(
            usuario=user, rol__nombre__in=["DIRECCIÓN", "SISTEMAS"]
        ).exists()

    def handle_no_permission(self):
        raise PermissionDenied("No tienes permiso para acceder a esta vista.")


class PermisoMedicoMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return UsuarioRol.objects.filter(
            usuario=user,
            rol__nombre__in=["MÉDICO", "DIRECCIÓN", "ENFERMERO", "SISTEMAS"],
        ).exists()

    def handle_no_permission(self):
        raise PermissionDenied("No tienes permiso para acceder a esta vista.")


class PermisoAdminMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return UsuarioRol.objects.filter(
            usuario=user,
            rol__nombre__in=["ADMINISTRACIÓN", "DIRECCIÓN", "SISTEMAS"],
        ).exists()

    def handle_no_permission(self):
        raise PermissionDenied("No tienes permiso para acceder a esta vista.")


class PermisoFarmaciaMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return UsuarioRol.objects.filter(
            usuario=user,
            rol__nombre__in=["FARMACIA", "DIRECCIÓN", "SISTEMAS", "LABORATORIO"],
        ).exists()

    def handle_no_permission(self):
        raise PermissionDenied("No tienes permiso para acceder a esta vista.")


class PermisoBasicoMixin(LoginRequiredMixin):
    # No necesitas test_func, basta con que esté logueado
    pass


# --- Decorador para permisos altos (Director, Sistemas, Superuser) ---
from django.contrib.auth.decorators import login_required, user_passes_test
from acceso.models import UsuarioRol


# --- Decorador para permisos altos ---
def permiso_alto_required(view_func):
    def tiene_permiso_alto(user):
        if user.is_superuser:
            return True
        return UsuarioRol.objects.filter(
            usuario=user, rol__nombre__in=["DIRECCIÓN", "SISTEMAS"]
        ).exists()

    return login_required(user_passes_test(tiene_permiso_alto)(view_func))


# --- Decorador para médicos y director ---
def permiso_medico_required(view_func):
    def tiene_permiso_medico(user):
        if user.is_superuser:
            return True
        return UsuarioRol.objects.filter(
            usuario=user,
            rol__nombre__in=["MÉDICO", "DIRECCIÓN", "ENFERMERO", "SISTEMAS"],
        ).exists()

    return login_required(user_passes_test(tiene_permiso_medico)(view_func))


# --- Decorador para administración ---
def permiso_admin_required(view_func):
    def tiene_permiso_admin(user):
        if user.is_superuser:
            return True
        return UsuarioRol.objects.filter(
            usuario=user,
            rol__nombre__in=["ADMINISTRACIÓN", "DIRECCIÓN", "SISTEMAS"],
        ).exists()

    return login_required(user_passes_test(tiene_permiso_admin)(view_func))


# --- Decorador para farmacia ---
def permiso_farmacia_required(view_func):
    def tiene_permiso_farmacia(user):
        if user.is_superuser:
            return True
        return UsuarioRol.objects.filter(
            usuario=user,
            rol__nombre__in=["FARMACIA", "DIRECCIÓN", "SISTEMAS", "LABORATORIO"],
        ).exists()

    return login_required(user_passes_test(tiene_permiso_farmacia)(view_func))


# --- Decorador para cualquier usuario autenticado ---
def permiso_basico_required(view_func):
    def tiene_permiso_basico(user):
        return user.is_authenticated

    return login_required(user_passes_test(tiene_permiso_basico)(view_func))


# importar decorador
"""
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from acceso.mixins import permiso_alto_required, permiso_medico_required, permiso_basico_required

@login_required
@user_passes_test(tiene_permiso_alto)
def auditoria_view(request):
    # lógica de auditoría
    ...


@permiso_alto_required
def auditoria_view(request):
    # Solo director, sistemas y superuser
    ...

@permiso_medico_required
def cita_view(request):
    # Solo médicos y director
    ...

@permiso_basico_required
def perfil_view(request):
    # Cualquier usuario autenticado
    ...


# importar en vistas basadas en clases
from acceso.mixins import PermisoAltoMixin

class AuditoriaListView(LoginRequiredMixin, PermisoAltoMixin, ListView):
    model = Auditoria
    template_name = "auditoria/lista.html"
    context_object_name = "auditorias"

"""
