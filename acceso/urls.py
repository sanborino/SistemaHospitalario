from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from .views import hospital

app_name = "acceso"

urlpatterns = [
    path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("registro/", views.registro, name="registro"),
    path("login/", views.login_usuario, name="login"),
    path("logout/", views.logout_usuario, name="logout"),
    path("Bienvenida/", hospital, name="hospitales"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # Usuarios
    path("usuarios/", views.usuario_lista, name="usuario_lista"),
    path("usuarios/crear/", views.usuario_crear, name="usuario_crear"),
    path("usuarios/<int:pk>/editar/", views.usuario_editar, name="usuario_editar"),
    path(
        "usuarios/<int:pk>/eliminar/", views.usuario_eliminar, name="usuario_eliminar"
    ),
    path("usuarios/<int:pk>/", views.usuario_detalle, name="usuario_detalle"),
    path(
        "usuarios/<int:usuario_id>/asignar-rol/",
        views.asignar_rol_usuario,
        name="asignar_rol_usuario",
    ),
    path(
        "usuarios/<int:usuario_id>/quitar-rol/<int:rol_id>/",
        views.quitar_rol_usuario,
        name="quitar_rol_usuario",
    ),
    # Roles
    path("roles/", views.rol_lista, name="rol_lista"),
    path("roles/crear/", views.rol_crear, name="rol_crear"),
    path("roles/<int:pk>/editar/", views.rol_editar, name="rol_editar"),
    path("roles/<int:pk>/eliminar/", views.rol_eliminar, name="rol_eliminar"),
    path("roles/<int:pk>/", views.rol_detalle, name="rol_detalle"),
    path(
        "roles/<int:rol_id>/asignar-permiso/",
        views.asignar_permiso_rol,
        name="asignar_permiso_rol",
    ),
    path(
        "roles/<int:rol_id>/quitar-permiso/<int:permiso_id>/",
        views.quitar_permiso_rol,
        name="quitar_permiso_rol",
    ),
    # Permisos
    path("permisos/", views.permiso_lista, name="permiso_lista"),
    path("permisos/crear/", views.permiso_crear, name="permiso_crear"),
    path("permisos/<int:pk>/editar/", views.permiso_editar, name="permiso_editar"),
    path(
        "permisos/<int:pk>/eliminar/", views.permiso_eliminar, name="permiso_eliminar"
    ),
    # Usuarios hospitales
    path(
        "hospitales/usuarios/", views.usuariohospital_list, name="usuariohospital_list"
    ),
    path("crear/", views.usuariohospital_create, name="usuariohospital_create"),
    path(
        "editar/<int:pk>/", views.usuariohospital_update, name="usuariohospital_update"
    ),
    path(
        "eliminar/<int:pk>/",
        views.usuariohospital_delete,
        name="usuariohospital_delete",
    ),
]
