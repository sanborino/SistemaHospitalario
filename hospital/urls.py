from django.urls import path
from .views import (
    HospitalListView,
    HospitalDetailView,
    HospitalCreateView,
    HospitalUpdateView,
    HospitalDeleteView,
)

app_name = "hospital"

urlpatterns = [
    path("lista/", HospitalListView.as_view(), name="lista_hospital"),
    path("nuevo/", HospitalCreateView.as_view(), name="crear_hospital"),
    path("<int:pk>/", HospitalDetailView.as_view(), name="detalle_hospital"),
    path("<int:pk>/editar/", HospitalUpdateView.as_view(), name="editar_hospital"),
    path("<int:pk>/eliminar/", HospitalDeleteView.as_view(), name="eliminar_hospital"),
]
