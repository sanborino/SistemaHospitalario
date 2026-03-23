from django.urls import path
from . import views
from .views import (
    AreaListView,
    AreaDetailView,
    AreaCreateView,
    AreaUpdateView,
    AreaDeleteView,
    HabitacionListView,
    HabitacionDetailView,
    HabitacionCreateView,
    HabitacionUpdateView,
    HabitacionDeleteView,
    infraestructura_dashboard,
)

app_name = "infraestructura"

urlpatterns = [
    path("", infraestructura_dashboard, name="dashboard"),
    path("areas/", AreaListView.as_view(), name="lista_area"),
    path("areas/nuevo/", AreaCreateView.as_view(), name="crear_area"),
    path("areas/<int:pk>/", AreaDetailView.as_view(), name="detalle_area"),
    path("areas/<int:pk>/editar/", AreaUpdateView.as_view(), name="editar_area"),
    path("areas/<int:pk>/eliminar/", AreaDeleteView.as_view(), name="eliminar_area"),
    path("habitaciones/", HabitacionListView.as_view(), name="lista_habitacion"),
    path(
        "habitaciones/nuevo/", HabitacionCreateView.as_view(), name="crear_habitacion"
    ),
    path(
        "habitaciones/<int:pk>/",
        HabitacionDetailView.as_view(),
        name="detalle_habitacion",
    ),
    path(
        "habitaciones/<int:pk>/editar/",
        HabitacionUpdateView.as_view(),
        name="editar_habitacion",
    ),
    path(
        "habitaciones/<int:pk>/eliminar/",
        HabitacionDeleteView.as_view(),
        name="eliminar_habitacion",
    ),
    path("habitaciones/", views.lista_habitaciones, name="lista_habitaciones"),
    path("camas/", views.lista_camas, name="infra_lista_camas"),
    path("camas/crear/", views.crear_cama, name="infra_crear_cama"),
    path("camas/editar/<int:cama_id>/", views.editar_cama, name="infra_editar_cama"),
    path(
        "camas/eliminar/<int:cama_id>/", views.eliminar_cama, name="infra_eliminar_cama"
    ),
]
