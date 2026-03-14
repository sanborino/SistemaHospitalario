from django.contrib import admin
from .models import Paciente


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "apellido",
        "hospital",
        "fecha_nacimiento",
        "sexo",
        "telefono",
        "tipo_sangre",
    )
    search_fields = (
        "nombre",
        "apellido",
        "telefono",
        "tipo_sangre",
    )
    list_filter = (
        "hospital",
        "sexo",
        "tipo_sangre",
    )
    ordering = ("apellido", "nombre")