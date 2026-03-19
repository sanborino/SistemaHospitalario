from django.db import models
from paciente.models import Paciente
from personal.models import Medico
from hospital.models import Hospital
from cita.models import Cita

# Create your models here.

class HistorialClinico(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)
    cita = models.OneToOneField(Cita, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True)
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Historial de {self.paciente} - {self.fecha}"
