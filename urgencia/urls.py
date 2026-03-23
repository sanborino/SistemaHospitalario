from django.urls import path
from .views import (
    UrgenciaListView,
    UrgenciaDetailView,
    UrgenciaCreateView,
    UrgenciaUpdateView,
    UrgenciaDeleteView,
    AtencionUrgenciaListView,
    AtencionUrgenciaDetailView,
    AtencionUrgenciaCreateView,
    AtencionUrgenciaUpdateView,
    AtencionUrgenciaDeleteView,
    AltaUrgenciaListView,
    AltaUrgenciaDetailView,
    AltaUrgenciaCreateView,
    AltaUrgenciaUpdateView,
    AltaUrgenciaDeleteView,
)

app_name = "urgencia"

urlpatterns = [
    path("urgencias/", UrgenciaListView.as_view(), name="lista_urgencia"),
    path("urgencias/nuevo/", UrgenciaCreateView.as_view(), name="crear_urgencia"),
    path("urgencias/<int:pk>/", UrgenciaDetailView.as_view(), name="detalle_urgencia"),
    path(
        "urgencias/<int:pk>/editar/",
        UrgenciaUpdateView.as_view(),
        name="editar_urgencia",
    ),
    path(
        "urgencias/<int:pk>/eliminar/",
        UrgenciaDeleteView.as_view(),
        name="eliminar_urgencia",
    ),
    path("atenciones/", AtencionUrgenciaListView.as_view(), name="lista_atencion"),
    path(
        "atenciones/nuevo/", AtencionUrgenciaCreateView.as_view(), name="crear_atencion"
    ),
    path(
        "atenciones/<int:pk>/",
        AtencionUrgenciaDetailView.as_view(),
        name="detalle_atencion",
    ),
    path(
        "atenciones/<int:pk>/editar/",
        AtencionUrgenciaUpdateView.as_view(),
        name="editar_atencion",
    ),
    path(
        "atenciones/<int:pk>/eliminar/",
        AtencionUrgenciaDeleteView.as_view(),
        name="eliminar_atencion",
    ),
    path("altas/", AltaUrgenciaListView.as_view(), name="lista_alta"),
    path("altas/nuevo/", AltaUrgenciaCreateView.as_view(), name="crear_alta"),
    path("altas/<int:pk>/", AltaUrgenciaDetailView.as_view(), name="detalle_alta"),
    path(
        "altas/<int:pk>/editar/", AltaUrgenciaUpdateView.as_view(), name="editar_alta"
    ),
    path(
        "altas/<int:pk>/eliminar/",
        AltaUrgenciaDeleteView.as_view(),
        name="eliminar_alta",
    ),
]
