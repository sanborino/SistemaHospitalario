from django.urls import path
from . import views

app_name = "facturacion"

urlpatterns = [
    path("", views.factura_lista, name="factura_lista"),
    path("crear/", views.factura_crear, name="factura_crear"),
    path("editar/<int:pk>/", views.factura_editar, name="factura_editar"),
    path(
        "eliminar/<int:pk>/", views.FacturaDeleteView.as_view(), name="factura_eliminar"
    ),
    path("detalle_factura/<int:pk>/", views.factura_detalle, name="factura_detalle"),
    path("detalle/crear/", views.detalle_crear, name="detalle_crear"),
    path("detalle/editar/<int:pk>/", views.detalle_editar, name="detalle_editar"),
    path("detalle/eliminar/<int:pk>/", views.detalle_eliminar, name="detalle_eliminar"),
    path("pago/crear/", views.pago_crear, name="pago_crear"),
    path("pago/editar/<int:pk>/", views.pago_editar, name="pago_editar"),
    path("pago/eliminar/<int:pk>/", views.pago_eliminar, name="pago_eliminar"),
    path(
        "generar_factura/paciente/<int:paciente_id>/",
        views.generar_factura_paciente,
        name="generar_factura_paciente",
    ),
]
