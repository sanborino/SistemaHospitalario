from django.urls import path
from .views import (
    MedicoListView,
    MedicoCreateView,
    MedicoUpdateView,
    MedicoDeleteView,
    EnfermeroListView,
    EnfermeroCreateView,
    EnfermeroUpdateView,
    EnfermeroDeleteView,
)
from . import views

app_name = "personal"

urlpatterns = [
    # Médicos
    path("medicos/", MedicoListView.as_view(), name="medico_list"),
    path("medicos/crear/", MedicoCreateView.as_view(), name="medico_create"),
    path("medicos/<int:pk>/editar/", MedicoUpdateView.as_view(), name="medico_edit"),
    path(
        "medicos/<int:pk>/eliminar/", MedicoDeleteView.as_view(), name="medico_delete"
    ),
    # Enfermeros
    path("enfermeros/", EnfermeroListView.as_view(), name="enfermero_list"),
    path("enfermeros/crear/", EnfermeroCreateView.as_view(), name="enfermero_create"),
    path(
        "enfermeros/<int:pk>/editar/",
        EnfermeroUpdateView.as_view(),
        name="enfermero_edit",
    ),
    path(
        "enfermeros/<int:pk>/eliminar/",
        EnfermeroDeleteView.as_view(),
        name="enfermero_delete",
    ),
    # Personal
    path("", views.PersonalListView.as_view(), name="personal_list"),
    path(
        "area/<str:area>/", views.PersonalListView.as_view(), name="personal_area_list"
    ),
    path("nuevo/", views.PersonalCreateView.as_view(), name="personal_create"),
    path(
        "editar/<int:pk>/", views.PersonalUpdateView.as_view(), name="personal_update"
    ),
    path(
        "eliminar/<int:pk>/", views.PersonalDeleteView.as_view(), name="personal_delete"
    ),
]
