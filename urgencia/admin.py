from django.contrib import admin
from .models import Urgencia, AtencionUrgencia, AltaUrgencia


class AtencionUrgenciaInline(admin.StackedInline):
    model = AtencionUrgencia
    extra = 0
    readonly_fields = ("fecha",)


class AltaUrgenciaInline(admin.StackedInline):
    model = AltaUrgencia
    extra = 0
    readonly_fields = ("fecha",)


@admin.register(Urgencia)
class UrgenciaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "paciente",
        "hospital",
        "fecha_ingreso",
        "nivel_triaje",
        "estado",
    )
    list_filter = ("hospital", "nivel_triaje", "estado", "fecha_ingreso")
    search_fields = (
        "paciente__nombre",
        "paciente__apellido",
        "motivo",
    )
    ordering = ("-fecha_ingreso",)
    inlines = [AtencionUrgenciaInline, AltaUrgenciaInline]


@admin.register(AtencionUrgencia)
class AtencionUrgenciaAdmin(admin.ModelAdmin):
    list_display = ("id", "urgencia", "medico", "fecha")
    search_fields = (
        "urgencia__id",
        "medico__nombre",
        "medico__apellido",
    )
    list_filter = ("fecha", "medico")
    readonly_fields = ("fecha",)
    ordering = ("-fecha",)


@admin.register(AltaUrgencia)
class AltaUrgenciaAdmin(admin.ModelAdmin):
    list_display = ("id", "urgencia", "fecha")
    search_fields = ("urgencia__id",)
    list_filter = ("fecha",)
    readonly_fields = ("fecha",)
    ordering = ("-fecha",)