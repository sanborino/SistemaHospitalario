from django.contrib import admin
from .models import Area, Habitacion

# -----------------------------
# Inline para Habitaciones
# -----------------------------

class HabitacionInline(admin.TabularInline):
    model = Habitacion
    extra = 1


# -----------------------------
# Admin de Area
# -----------------------------
@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'hospital', 'nombre', 'tipo')
    search_fields = ('nombre', 'tipo', 'hospital__nombre')
    list_filter = ('hospital', 'tipo')
    ordering = ('nombre',)
    inlines = [HabitacionInline]

# -----------------------------
# Admin de Habitacion
# -----------------------------
@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'hospital', 'area', 'numero', 'estado')
    search_fields = ('numero', 'estado', 'area__nombre', 'hospital__nombre')
    list_filter = ('hospital', 'area', 'estado')
    ordering = ('area', 'numero')
