from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler403, handler500
from SistemaHospitalario import views

handler404 = "SistemaHospitalario.views.custom_404"
handler403 = "SistemaHospitalario.views.custom_403"
handler500 = "SistemaHospitalario.views.custom_500"


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
    path("turnos/", include("turno.urls", namespace="turno")),
    path("auditoria/", include("auditoria.urls", namespace="auditoria")),
    path("factura/", include("facturacion.urls", namespace="facturacion")),
    path("farmacia/", include("farmacia.urls", namespace="farmacia")),
]
