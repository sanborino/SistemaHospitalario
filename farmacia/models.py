from django.db import models
from paciente.models import Paciente
from personal.models import Medico, Enfermero
from hospital.models import Hospital

# Create your models here.

class Medicamento(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    presentacion = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre


class Receta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField(auto_now_add=True)
    indicaciones = models.TextField()

    def __str__(self):
        return f"Receta {self.id} - {self.paciente}"


class RecetaDetalle(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.medicamento} x {self.cantidad}"


class Dispensacion(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    entregado_por = models.ForeignKey(Enfermero, on_delete=models.SET_NULL, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Dispensación {self.id} - Receta {self.receta.id}"
    
    class Meta:
        verbose_name = "Dispensación"
        verbose_name_plural = "Dispensaciones"