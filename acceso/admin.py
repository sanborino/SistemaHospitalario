from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Rol, Permiso, Usuario, UsuarioRol, RolPermiso, UsuarioHospital
)

# -----------------------------
# Inline para relaciones
# -----------------------------

class UsuarioRolInline(admin.TabularInline):
    model = UsuarioRol
    extra = 1

 
class UsuarioHospitalInline(admin.TabularInline):
    model = UsuarioHospital
    extra = 1


class RolPermisoInline(admin.TabularInline):
    model = RolPermiso
    extra = 1


# -----------------------------
# Admin de modelos principales
# -----------------------------

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
    inlines = [RolPermisoInline]

@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

@admin.register(UsuarioRol)
class UsuarioRolAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'rol')
    search_fields = ('usuario__username', 'rol__nombre')
    list_filter = ('rol',)

@admin.register(RolPermiso)
class RolPermisoAdmin(admin.ModelAdmin):
    list_display = ('id', 'rol', 'permiso')
    search_fields = ('rol__nombre', 'permiso__nombre')
    list_filter = ('rol',)


@admin.register(UsuarioHospital)
class UsuarioHospitalAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'hospital')
    search_fields = ('usuario__username', 'hospital__nombre')
    list_filter = ('hospital',)
    
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ("id", "username", "email", "estado", "is_staff", "is_active")
    list_filter = ("estado", "is_staff", "is_active")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Permisos", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Estado", {"fields": ("estado",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("username", "email")
    ordering = ("username",)