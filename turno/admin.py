from django.contrib import admin
from .models import Turno, TurnoPersonal, Asistencia


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "hospital", "hora_inicio", "hora_fin")
    search_fields = ("nombre",)
    list_filter = ("hospital",)
    ordering = ("nombre",)


@admin.register(TurnoPersonal)
class TurnoPersonalAdmin(admin.ModelAdmin):
    list_display = ("turno", "fecha", "medico", "enfermero")
    list_filter = ("turno", "fecha")
    search_fields = (
        "turno__nombre",
        "medico__nombre",
        "medico__apellido",
        "enfermero__nombre",
        "enfermero__apellido",
    )
    autocomplete_fields = ("turno", "medico", "enfermero")
    ordering = ("-fecha",)


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "fecha", "hora_entrada", "hora_salida")
    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
    )
    list_filter = ("fecha",)
    ordering = ("-fecha", "hora_entrada")