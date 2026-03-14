from django.db import models
from paciente.models import Paciente
from personal.models import Medico
from hospital.models import Hospital
# Create your models here.


class Cita(models.Model):
    ESTADOS = [
        ("programada", "Programada"),
        ("atendida", "Atendida"),
        ("cancelada", "Cancelada"),
    ]
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="programada")

    def __str__(self):
        return f"Cita {self.fecha} - {self.paciente}"