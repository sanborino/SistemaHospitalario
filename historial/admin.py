from django.contrib import admin
from .models import HistorialClinico


@admin.register(HistorialClinico)
class HistorialClinicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'hospital', 'paciente', 'medico', 'fecha')
    search_fields = (
        'paciente__nombre',
        'paciente__apellido',
        'medico__nombre',
        'medico__apellido',
        'diagnostico',
        'tratamiento',
        'notas',
    )
    list_filter = ('hospital', 'medico', 'fecha')
    ordering = ('-fecha',)