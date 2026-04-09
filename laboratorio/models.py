from django.db import models
from paciente.models import Paciente
from personal.models import Medico
from hospital.models import Hospital
from django.conf import settings

# Create your models here.


class Estudio(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class SolicitudLaboratorio(models.Model):
    ESTADO_PENDIENTE = "pendiente"
    ESTADO_FINALIZADO = "finalizado"

    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, "Pendiente"),
        (ESTADO_FINALIZADO, "Finalizado"),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_PENDIENTE,
    )

    def __str__(self):
        return f"Solicitud {self.id} - {self.paciente}"


class SolicitudDetalle(models.Model):
    solicitud = models.ForeignKey(SolicitudLaboratorio, on_delete=models.CASCADE)
    estudio = models.ForeignKey(Estudio, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.estudio}"


class ResultadoLaboratorio(models.Model):
    solicitud = models.ForeignKey(SolicitudLaboratorio, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    resultados = models.TextField()
    firmado_por = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Resultado {self.id} - Solicitud {self.solicitud.id}"
