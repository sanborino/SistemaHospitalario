from django.contrib import admin
from .models import Auditoria


@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'tabla', 'operacion', 'registro_id', 'fecha')
    search_fields = ('tabla', 'operacion', 'registro_id')
    list_filter = ('tabla', 'operacion', 'fecha')
    ordering = ('-fecha',)
    
# Configuración del panel
title = "Sistema Hospitalario"
subtitle = "Panel de gestión"

admin.site.site_header = title
admin.site.site_title = title
admin.site.index_title = subtitle