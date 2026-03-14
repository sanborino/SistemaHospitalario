from django.db import models
from paciente.models import Paciente
from personal.models import Medico
from hospital.models import Hospital

# Create your models here.

class Urgencia(models.Model):

    NIVELES_TRIAJE = [
        ("CRITICO", "Crítico (Nivel 1)"),
        ("EMERGENTE", "Emergente (Nivel 2)"),
        ("URGENTE", "Urgente (Nivel 3)"),
        ("NO_URGENTE", "No urgente (Nivel 4)"),
        ("AMBULATORIO", "Ambulatorio (Nivel 5)"),
    ]

    ESTADOS = [
        ("EN_ATENCION", "En atención"),
        ("EN_OBSERVACION", "En observación"),
        ("DADO_DE_ALTA", "Dado de alta"),
        ("HOSPITALIZADO", "Hospitalizado"),
        ("REFERIDO", "Referido a otro centro"),
        ("CERRADO", "Caso cerrado"),
    ]

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    nivel_triaje = models.CharField(max_length=20, choices=NIVELES_TRIAJE)
    motivo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="EN_ATENCION")

    def __str__(self):
        return f"Urgencia {self.id} - {self.paciente}"


class AtencionUrgencia(models.Model):
    urgencia = models.ForeignKey(Urgencia, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    notas = models.TextField()

    def __str__(self):
        return f"Atención {self.id} - Urgencia {self.urgencia.id}"


class AltaUrgencia(models.Model):
    urgencia = models.ForeignKey(Urgencia, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    diagnostico_final = models.TextField()
    recomendaciones = models.TextField()

    def __str__(self):
        return f"Alta {self.id} - Urgencia {self.urgencia.id}"
    