from django.db import models
from paciente.models import Paciente
from hospital.models import Hospital
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


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
    solicitud = models.ForeignKey(
        "laboratorio.SolicitudLaboratorio",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="PENDIENTE")
    origen_estudio = models.BooleanField(default=False)

    def __str__(self):
        return f"Factura #{self.id} - {self.paciente}"


class FacturaDetalle(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"Detalle {self.id} - Factura {self.factura.id}"


class Pago(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=50)

    def __str__(self):
        return f"Pago {self.id} - Factura {self.factura.id}"


class Cargo(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    factura = models.ForeignKey(
        Factura,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cargos",
    )

    descripcion = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    fecha = models.DateTimeField(auto_now_add=True)
    facturado = models.BooleanField(default=False)

    # vínculos opcionales al origen del cargo
    cama = models.ForeignKey(
        "infraestructura.Cama",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    dispensacion = models.ForeignKey(
        "farmacia.Dispensacion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    urgencia = models.ForeignKey(
        "urgencia.Urgencia",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    laboratorio = models.ForeignKey(
        "laboratorio.SolicitudLaboratorio",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.descripcion} - {self.paciente}"


def recalcular_total_factura(factura):
    subtotal = sum(d.cantidad * d.precio_unitario for d in factura.detalles.all())
    factura.total = subtotal
    factura.save()


@receiver(post_save, sender=FacturaDetalle)
def actualizar_total_factura(sender, instance, **kwargs):
    recalcular_total_factura(instance.factura)


@receiver(post_delete, sender=FacturaDetalle)
def actualizar_total_factura_delete(sender, instance, **kwargs):
    recalcular_total_factura(instance.factura)
