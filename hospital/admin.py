from django.contrib import admin
from .models import Hospital


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion', 'telefono', 'correo', 'codigo')
    search_fields = ('nombre', 'direccion', 'telefono', 'correo', 'codigo')
    list_filter = ('codigo',)
    ordering = ('nombre',)