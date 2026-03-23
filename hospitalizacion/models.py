from django.db import models
from django.utils import timezone
from infraestructura.models import Cama
from paciente.models import Paciente  # ajusta si tu app se llama distinto


class AsignacionCama(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    cama = models.ForeignKey(Cama, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha_ingreso"]

    def __str__(self):
        return f"{self.paciente} → {self.cama}"
