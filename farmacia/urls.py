from django.urls import path
from . import views
from .views import dispensacion_create

app_name = "farmacia"

urlpatterns = [
    # Medicamentos
    path("medicamentos/", views.MedicamentoListView.as_view(), name="medicamento_list"),
    path(
        "medicamentos/nuevo/",
        views.MedicamentoCreateView.as_view(),
        name="medicamento_create",
    ),
    path(
        "medicamentos/editar/<int:pk>/",
        views.MedicamentoUpdateView.as_view(),
        name="medicamento_edit",
    ),
    path(
        "medicamentos/<int:pk>/",
        views.MedicamentoDetailView.as_view(),
        name="medicamento_detalle",
    ),
    path(
        "medicamentos/<int:pk>/eliminar/",
        views.MedicamentoDeleteView.as_view(),
        name="medicamento_eliminar",
    ),
    # Recetas
    path("recetas/", views.RecetaListView.as_view(), name="receta_list"),
    path("recetas/nueva/", views.RecetaCreateView.as_view(), name="receta_create"),
    path("recetas/<int:pk>/", views.RecetaDetailView.as_view(), name="receta_detalle"),
    path(
        "recetas/<int:receta_id>/agregar-detalle/",
        views.RecetaDetalleCreateView.as_view(),
        name="receta_detalle_add",
    ),
    path(
        "recetas/detalle/<int:pk>/edit/",
        views.RecetaDetalleUpdateView.as_view(),
        name="receta_detalle_edit",
    ),
    path(
        "recetas/detalle/<int:pk>/delete/",
        views.RecetaDetalleDeleteView.as_view(),
        name="receta_detalle_delete",
    ),
    path(
        "recetas/<int:pk>/eliminar/",
        views.RecetaDeleteView.as_view(),
        name="receta_delete",
    ),
    # Dispensaciones
    path(
        "dispensaciones/",
        views.DispensacionListView.as_view(),
        name="dispensacion_list",
    ),
    path(
        "dispensaciones/nueva/",
        views.DispensacionCreateView.as_view(),
        name="dispensacion_create",
    ),
    path("dispensar/<int:receta_id>/", dispensacion_create, name="dispensar_receta"),
    path(
        "dispensaciones/<int:pk>/",
        views.DispensacionDetailView.as_view(),
        name="dispensacion_detalle",
    ),
]
