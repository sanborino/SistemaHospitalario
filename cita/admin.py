from django.contrib import admin
from .models import Cita


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('id', 'hospital', 'paciente', 'medico', 'fecha', 'hora', 'estado')
    search_fields = (
        'paciente__nombre',
        'paciente__apellido',
        'medico__nombre',
        'medico__apellido',
        'hospital__nombre',
        'motivo',
    )
    list_filter = ('hospital', 'medico', 'estado', 'fecha')
    ordering = ('-fecha', '-hora')