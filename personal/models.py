from django.db import models
from hospital.models import Hospital
from django.conf import settings

# Create your models here.


class Medico(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    numero_licencia = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()

    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido}"


class Enfermero(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    turno = models.CharField(max_length=50)

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Personal(models.Model):
    AREAS = [
        ("laboratorio", "Laboratorio"),
        ("sistemas", "Sistemas"),
        ("administracion", "Administración"),
        ("farmacia", "Farmacia"),
        ("mantenimiento", "Mantenimiento"),
        ("direccion", "Dirección"),
    ]

    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    area = models.CharField(max_length=20, choices=AREAS)
    estado = models.BooleanField(default=True)

    # Llaves foráneas
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="personal"
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="personal"
    )

    def __str__(self):
        return f"{self.nombre} ({self.get_area_display()})"
