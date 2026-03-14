from django.contrib import admin
from .models import Factura, FacturaDetalle, Pago


# -----------------------------
# Inlines
# -----------------------------

class FacturaDetalleInline(admin.TabularInline):
    model = FacturaDetalle
    extra = 1


class PagoInline(admin.TabularInline):
    model = Pago
    extra = 1


# -----------------------------
# Admin principal: Factura
# -----------------------------

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'hospital', 'paciente', 'fecha', 'total', 'estado')
    search_fields = (
        'paciente__nombre',
        'paciente__apellido',
        'hospital__nombre',
        'estado',
    )
    list_filter = ('hospital', 'estado', 'fecha')
    ordering = ('-fecha',)
    inlines = [FacturaDetalleInline, PagoInline]


# -----------------------------
# Admin de FacturaDetalle
# -----------------------------

@admin.register(FacturaDetalle)
class FacturaDetalleAdmin(admin.ModelAdmin):
    list_display = ('id', 'factura', 'descripcion', 'cantidad', 'precio_unitario')
    search_fields = ('descripcion', 'factura__id')
    list_filter = ('factura',)


# -----------------------------
# Admin de Pago
# -----------------------------

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'factura', 'fecha', 'monto', 'metodo')
    search_fields = ('factura__id', 'metodo')
    list_filter = ('metodo', 'fecha')
    ordering = ('-fecha',)