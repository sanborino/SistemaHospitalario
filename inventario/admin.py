from django.contrib import admin
from .models import Insumo, MovimientoInventario


# -----------------------------
# Inline para movimientos
# -----------------------------

class MovimientoInventarioInline(admin.TabularInline):
    model = MovimientoInventario
    extra = 1
    readonly_fields = ('fecha',)


# -----------------------------
# Admin de Insumo
# -----------------------------

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('id', 'hospital', 'nombre', 'unidad', 'stock')
    search_fields = ('nombre', 'unidad', 'hospital__nombre')
    list_filter = ('hospital', 'unidad')
    ordering = ('nombre',)
    inlines = [MovimientoInventarioInline]


# -----------------------------
# Admin de MovimientoInventario
# -----------------------------

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'insumo', 'tipo', 'cantidad', 'fecha', 'realizado_por')
    search_fields = (
        'insumo__nombre',
        'realizado_por__username',
        'tipo',
    )
    list_filter = ('tipo', 'fecha', 'realizado_por')
    ordering = ('-fecha',)
    readonly_fields = ('fecha',)