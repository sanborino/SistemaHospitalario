from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),    
    path('', include("acceso.urls")),
    path('hospital/', include("hospital.urls")),
    path('paciente/', include("paciente.urls")),
]
