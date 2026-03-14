from django.contrib import admin
from .models import Estudio, SolicitudLaboratorio, SolicitudDetalle, ResultadoLaboratorio


class SolicitudDetalleInline(admin.TabularInline):
    model = SolicitudDetalle
    extra = 1


class ResultadoLaboratorioInline(admin.StackedInline):
    model = ResultadoLaboratorio
    extra = 0
    readonly_fields = ("fecha",)


@admin.register(Estudio)
class EstudioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "hospital", "precio")
    search_fields = ("nombre",)
    list_filter = ("hospital",)


@admin.register(SolicitudLaboratorio)
class SolicitudLaboratorioAdmin(admin.ModelAdmin):
    list_display = ("id", "paciente", "medico", "fecha", "estado")
    list_filter = ("estado", "fecha")
    search_fields = ("paciente__nombre", "medico__nombre")
    inlines = [SolicitudDetalleInline, ResultadoLaboratorioInline]


@admin.register(SolicitudDetalle)
class SolicitudDetalleAdmin(admin.ModelAdmin):
    list_display = ("solicitud", "estudio")
    search_fields = ("solicitud__id", "estudio__nombre")


@admin.register(ResultadoLaboratorio)
class ResultadoLaboratorioAdmin(admin.ModelAdmin):
    list_display = ("id", "solicitud", "fecha", "firmado_por")
    readonly_fields = ("fecha",)
    search_fields = ("solicitud__id", "firmado_por__nombre")