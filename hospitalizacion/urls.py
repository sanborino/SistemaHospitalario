from django.urls import path
from . import views

app_name = "hospitalizacion"

urlpatterns = [
    path("asignar/<int:paciente_id>/", views.asignar_cama, name="asignar_cama"),
    path("liberar/<int:asignacion_id>/", views.liberar_cama, name="liberar_cama"),
    path("trasladar/<int:asignacion_id>/", views.trasladar_cama, name="trasladar_cama"),
    path("historial/", views.historial_asignaciones, name="historial_asignaciones"),
]
