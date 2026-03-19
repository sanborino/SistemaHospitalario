from django.urls import path
from .views import (
    CitaListView, CitaDetailView,
    CitaCreateView, CitaUpdateView, CitaDeleteView,
    CitaCalendarioView
)

app_name = "cita"

urlpatterns = [
    path("", CitaListView.as_view(), name="lista_cita"),
    path("nuevo/", CitaCreateView.as_view(), name="crear_cita"),
    path("calendario/", CitaCalendarioView.as_view(), name="calendario_cita"),
    path("<int:pk>/", CitaDetailView.as_view(), name="detalle_cita"),
    path("<int:pk>/editar/", CitaUpdateView.as_view(), name="editar_cita"),
    path("<int:pk>/eliminar/", CitaDeleteView.as_view(), name="eliminar_cita"),
]