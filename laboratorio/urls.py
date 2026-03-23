from django.urls import path
from .views import (
    EstudioListView,
    EstudioDetailView,
    EstudioCreateView,
    EstudioUpdateView,
    EstudioDeleteView,
    SolicitudListView,
    SolicitudDetailView,
    SolicitudCreateView,
    SolicitudUpdateView,
    SolicitudDeleteView,
    ResultadoListView,
    ResultadoDetailView,
    ResultadoCreateView,
    ResultadoUpdateView,
    ResultadoDeleteView,
)

app_name = "laboratorio"

urlpatterns = [
    path("estudios/", EstudioListView.as_view(), name="lista_estudio"),
    path("estudios/nuevo/", EstudioCreateView.as_view(), name="crear_estudio"),
    path("estudios/<int:pk>/", EstudioDetailView.as_view(), name="detalle_estudio"),
    path(
        "estudios/<int:pk>/editar/", EstudioUpdateView.as_view(), name="editar_estudio"
    ),
    path(
        "estudios/<int:pk>/eliminar/",
        EstudioDeleteView.as_view(),
        name="eliminar_estudio",
    ),
    path("solicitudes/", SolicitudListView.as_view(), name="lista_solicitud"),
    path("solicitudes/nuevo/", SolicitudCreateView.as_view(), name="crear_solicitud"),
    path(
        "solicitudes/<int:pk>/", SolicitudDetailView.as_view(), name="detalle_solicitud"
    ),
    path(
        "solicitudes/<int:pk>/editar/",
        SolicitudUpdateView.as_view(),
        name="editar_solicitud",
    ),
    path(
        "solicitudes/<int:pk>/eliminar/",
        SolicitudDeleteView.as_view(),
        name="eliminar_solicitud",
    ),
    path("resultados/", ResultadoListView.as_view(), name="lista_resultado"),
    path("resultados/nuevo/", ResultadoCreateView.as_view(), name="crear_resultado"),
    path(
        "resultados/<int:pk>/", ResultadoDetailView.as_view(), name="detalle_resultado"
    ),
    path(
        "resultados/<int:pk>/editar/",
        ResultadoUpdateView.as_view(),
        name="editar_resultado",
    ),
    path(
        "resultados/<int:pk>/eliminar/",
        ResultadoDeleteView.as_view(),
        name="eliminar_resultado",
    ),
]
