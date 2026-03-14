from django.db import models
from acceso.models import Usuario
from hospital.models import Hospital

# Create your models here.

class Insumo(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    unidad = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class MovimientoInventario(models.Model):
    TIPO_MOV = [
        ("entrada", "Entrada"),
        ("salida", "Salida"),
    ]

    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_MOV)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    realizado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.insumo} ({self.cantidad})"
    
    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimiento de Inventarios"