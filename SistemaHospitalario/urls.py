from django.contrib import admin
from django.urls import path, include
from SistemaHospitalario.views import test_404

handler404 = "SistemaHospitalario.views.custom_404"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("acceso.urls", namespace="acceso")),
    path("acceso/", include("django.contrib.auth.urls")),
    path("hospital/", include("hospital.urls", namespace="hospital")),
    path(
        "hospitalizacion/", include("hospitalizacion.urls", namespace="hospitalizacion")
    ),
    path("paciente/", include("paciente.urls", namespace="paciente")),
    path("historial/", include("historial.urls", namespace="historial")),
    path("citas/", include("cita.urls", namespace="cita")),
    path("personal/", include("personal.urls", namespace="personal")),
    path(
        "infraestructura/", include("infraestructura.urls", namespace="infraestructura")
    ),
    path("inventario/", include("inventario.urls", namespace="inventario")),
    path("laboratorio/", include("laboratorio.urls", namespace="laboratorio")),
    path("urgencia/", include("urgencia.urls", namespace="urgencia")),
    path("test-404/", test_404),
    path("turnos/", include("turno.urls", namespace="turno")),
    path("auditoria/", include("auditoria.urls", namespace="auditoria")),
    path("factura/", include("facturacion.urls", namespace="facturacion")),
    path("farmacia/", include("farmacia.urls", namespace="farmacia")),
]
