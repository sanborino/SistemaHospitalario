from django.db import models
from hospital.models import Hospital

# Create your models here.


class Paciente(models.Model):
    TIPOS_SANGRE = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]

    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=20)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    contacto_emergencia = models.CharField(max_length=100)
    tipo_sangre = models.CharField(max_length=3, choices=TIPOS_SANGRE)
    alergias = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    