from django.urls import path
from .views import (
    MedicoListView, MedicoCreateView, MedicoUpdateView, MedicoDeleteView,
    EnfermeroListView, EnfermeroCreateView, EnfermeroUpdateView, EnfermeroDeleteView
)

app_name = "personal"

urlpatterns = [
    # Médicos
    path("medicos/", MedicoListView.as_view(), name="medico_list"),
    path("medicos/crear/", MedicoCreateView.as_view(), name="medico_create"),
    path("medicos/<int:pk>/editar/", MedicoUpdateView.as_view(), name="medico_edit"),
    path("medicos/<int:pk>/eliminar/", MedicoDeleteView.as_view(), name="medico_delete"),

    # Enfermeros
    path("enfermeros/", EnfermeroListView.as_view(), name="enfermero_list"),
    path("enfermeros/crear/", EnfermeroCreateView.as_view(), name="enfermero_create"),
    path("enfermeros/<int:pk>/editar/", EnfermeroUpdateView.as_view(), name="enfermero_edit"),
    path("enfermeros/<int:pk>/eliminar/", EnfermeroDeleteView.as_view(), name="enfermero_delete"),
]
