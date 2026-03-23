from django.urls import path
from .views import (
    inventario_dashboard,
    InsumoListView, InsumoDetailView, InsumoCreateView, InsumoUpdateView, InsumoDeleteView,
    MovimientoListView, MovimientoDetailView, MovimientoCreateView, MovimientoUpdateView, MovimientoDeleteView,
)

app_name = "inventario"

urlpatterns = [
    path("", inventario_dashboard, name="dashboard"),

    path("insumos/", InsumoListView.as_view(), name="lista_insumo"),
    path("insumos/nuevo/", InsumoCreateView.as_view(), name="crear_insumo"),
    path("insumos/<int:pk>/", InsumoDetailView.as_view(), name="detalle_insumo"),
    path("insumos/<int:pk>/editar/", InsumoUpdateView.as_view(), name="editar_insumo"),
    path("insumos/<int:pk>/eliminar/", InsumoDeleteView.as_view(), name="eliminar_insumo"),

    path("movimientos/", MovimientoListView.as_view(), name="lista_movimiento"),
    path("movimientos/nuevo/", MovimientoCreateView.as_view(), name="crear_movimiento"),
    path("movimientos/<int:pk>/", MovimientoDetailView.as_view(), name="detalle_movimiento"),
    path("movimientos/<int:pk>/editar/", MovimientoUpdateView.as_view(), name="editar_movimiento"),
    path("movimientos/<int:pk>/eliminar/", MovimientoDeleteView.as_view(), name="eliminar_movimiento"),
]