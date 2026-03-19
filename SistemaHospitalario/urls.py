from django.contrib import admin
from django.urls import path, include
from SistemaHospitalario.views import test_404

handler404 = "SistemaHospitalario.views.custom_404"

from django.http import HttpResponseNotFound

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', include("acceso.urls")),
    path('acceso/', include('django.contrib.auth.urls')),
    path('hospital/', include("hospital.urls")),
    path('pacientes/', include("paciente.urls", namespace="paciente")),
    path("historial/", include("historial.urls")),
    path("citas/", include("cita.urls", namespace="cita")),
    path("personal/", include("personal.urls")),
    path("test-404/", test_404),
    path('turnos/', include('turno.urls')),
    path('auditoria/', include('auditoria.urls')),

]

