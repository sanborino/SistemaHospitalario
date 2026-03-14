from django.urls import path
from .views import PacienteListView, PacienteCreateView

app_name = "paciente"

urlpatterns = [
    path('listado/', PacienteListView.as_view(), name="lista_pacientes"),
    path('crear/', PacienteCreateView.as_view(), name="crear_paciente"),
]