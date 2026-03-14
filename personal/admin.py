from django.contrib import admin
from .models import Medico, Enfermero


@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "apellido",
        "hospital",
        "especialidad",
        "numero_licencia",
        "telefono",
        "correo",
    )
    search_fields = (
        "nombre",
        "apellido",
        "numero_licencia",
        "especialidad",
        "correo",
    )
    list_filter = (
        "hospital",
        "especialidad",
    )
    ordering = ("apellido", "nombre")
    autocomplete_fields = ("usuario", "hospital")


@admin.register(Enfermero)
class EnfermeroAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "apellido",
        "turno",
        "usuario",
    )
    search_fields = (
        "nombre",
        "apellido",
        "turno",
    )
    list_filter = ("turno",)
    ordering = ("apellido", "nombre")
    autocomplete_fields = ("usuario",)