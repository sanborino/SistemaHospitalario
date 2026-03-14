from django.db import models
from paciente.models import Paciente
from hospital.models import Hospital

# Create your models here.

class Factura(models.Model):

    ESTADOS = [
        ("PENDIENTE", "Pendiente"),
        ("PAGADA", "Pagada"),
        ("ANULADA", "Anulada"),
        ("EN_PROCESO", "En proceso"),
    ]

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="PENDIENTE")

    def __str__(self):
        return f"Factura #{self.id} - {self.paciente}"


class FacturaDetalle(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id} - Factura {self.factura.id}"


class Pago(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=50)

    def __str__(self):
        return f"Pago {self.id} - Factura {self.factura.id}"