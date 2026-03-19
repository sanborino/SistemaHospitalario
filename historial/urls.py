from django.urls import path
from .views import (
    HistorialListView, HistorialDetailView,
    HistorialCreateView, HistorialUpdateView, HistorialDeleteView
)

app_name = "historial"

urlpatterns = [
    path("", HistorialListView.as_view(), name="lista_historial"),
    path("nuevo/", HistorialCreateView.as_view(), name="crear_historial"),
    path("<int:pk>/", HistorialDetailView.as_view(), name="detalle_historial"),
    path("<int:pk>/editar/", HistorialUpdateView.as_view(), name="editar_historial"),
    path("<int:pk>/eliminar/", HistorialDeleteView.as_view(), name="eliminar_historial"),
]