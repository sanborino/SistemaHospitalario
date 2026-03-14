from django.contrib import admin
from .models import Medicamento, Receta, RecetaDetalle, Dispensacion


# -----------------------------
# Inlines
# -----------------------------

class RecetaDetalleInline(admin.TabularInline):
    model = RecetaDetalle
    extra = 1


class DispensacionInline(admin.TabularInline):
    model = Dispensacion
    extra = 1


# -----------------------------
# Admin de Medicamento
# -----------------------------

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'hospital', 'nombre', 'presentacion', 'stock', 'precio')
    search_fields = ('nombre', 'presentacion', 'hospital__nombre')
    list_filter = ('hospital',)
    ordering = ('nombre',)


# -----------------------------
# Admin de Receta
# -----------------------------

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'medico', 'fecha')
    search_fields = (
        'paciente__nombre',
        'paciente__apellido',
        'medico__nombre',
        'medico__apellido',
        'indicaciones',
    )
    list_filter = ('medico', 'fecha')
    ordering = ('-fecha',)
    inlines = [RecetaDetalleInline, DispensacionInline]


# -----------------------------
# Admin de RecetaDetalle
# -----------------------------

@admin.register(RecetaDetalle)
class RecetaDetalleAdmin(admin.ModelAdmin):
    list_display = ('id', 'receta', 'medicamento', 'cantidad')
    search_fields = ('receta__id', 'medicamento__nombre')
    list_filter = ('medicamento',)


# -----------------------------
# Admin de Dispensacion
# -----------------------------

@admin.register(Dispensacion)
class DispensacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'receta', 'fecha', 'entregado_por')
    search_fields = (
        'receta__id',
        'entregado_por__nombre',
        'entregado_por__apellido',
        'observaciones',
    )
    list_filter = ('fecha', 'entregado_por')
    ordering = ('-fecha',)