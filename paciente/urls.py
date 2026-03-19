from django.urls import path
from .views import (
    PacienteListView, PacienteDetailView,
    PacienteCreateView, PacienteUpdateView, PacienteDeleteView
)

app_name = "paciente"

urlpatterns = [
    path("", PacienteListView.as_view(), name="lista_paciente"),
    path("nuevo/", PacienteCreateView.as_view(), name="crear_paciente"),
    path("<int:pk>/", PacienteDetailView.as_view(), name="detalle_paciente"),
    path("<int:pk>/editar/", PacienteUpdateView.as_view(), name="editar_paciente"),
    path("<int:pk>/eliminar/", PacienteDeleteView.as_view(), name="eliminar_paciente"),
]