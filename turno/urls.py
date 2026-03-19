from django.urls import path
from .views import (
    TurnoListView, TurnoCreateView, TurnoUpdateView, TurnoDeleteView,
    TurnoPersonalListView, TurnoPersonalCreateView, TurnoPersonalUpdateView, TurnoPersonalDeleteView,
    AsistenciaListView, AsistenciaCreateView, AsistenciaUpdateView, AsistenciaDeleteView
)

app_name = "turno"

urlpatterns = [
    # Turnos
    path('turnos/', TurnoListView.as_view(), name='turno_list'),
    path('turnos/nuevo/', TurnoCreateView.as_view(), name='turno_create'),
    path('turnos/editar/<int:pk>/', TurnoUpdateView.as_view(), name='turno_update'),
    path('turnos/eliminar/<int:pk>/', TurnoDeleteView.as_view(), name='turno_delete'),

    # Turno Personal
    path('turnopersonal/', TurnoPersonalListView.as_view(), name='turnopersonal_list'),
    path('turnopersonal/nuevo/', TurnoPersonalCreateView.as_view(), name='turnopersonal_create'),
    path('turnopersonal/editar/<int:pk>/', TurnoPersonalUpdateView.as_view(), name='turnopersonal_update'),
    path('turnopersonal/eliminar/<int:pk>/', TurnoPersonalDeleteView.as_view(), name='turnopersonal_delete'),

    # Asistencia
    path('asistencia/', AsistenciaListView.as_view(), name='asistencia_list'),
    path('asistencia/nuevo/', AsistenciaCreateView.as_view(), name='asistencia_create'),
    path('asistencia/editar/<int:pk>/', AsistenciaUpdateView.as_view(), name='asistencia_update'),
    path('asistencia/eliminar/<int:pk>/', AsistenciaDeleteView.as_view(), name='asistencia_delete'),
]