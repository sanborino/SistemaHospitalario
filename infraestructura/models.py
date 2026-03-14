from django.db import models
from hospital.models import Hospital

# Create your models here.

class Area(models.Model):
    
    TIPOS = [
        ("ATENCIÓN CRÍTICA", "Atención crítica"),
        ("HOSPITALIZACIÓN", "Hospitalización"),
        ("CONSULTA", "Consulta"),
        ("DIAGNÓSTICO", "Diagnóstico"),
        ("ADMINISTRATIVA", "Administrativa"),
    ]

    NOMBRES = [
        ("URGENCIAS", "Urgencias"),
        ("PEDIATRÍA", "Pediatría"),
        ("OBSTETTRICIA", " Obstetricia"),
        ("UCI", "UCI"),
        ("HOSPITALIZACIÓN", "Hospitalización"),
        ("QUIRÓFANOS", "Quirófanos"),
        ("COSULTA EXTERNA", "Consulta externa"),
    ]
    
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, choices=NOMBRES, default="URGENCIAS")
    tipo = models.CharField(max_length=100, choices=TIPOS, default="ATENCIÓN CRÍTICA")

    def __str__(self):
        return self.nombre

class Habitacion(models.Model):
    
    ESTADOS = [
        ("ACTIVA", "Activa"),
        ("INACTIVA", "Inactiva"),
        ("EN_MANTENIMIENTO", "En mantenimiento"),
        ("DISPONIBLE", "Disponible"),
        ("OCUPADA", "Ocupada"),
        ("EN LIMPIEZA", "En limpieza"),
        ("FUERA DE SERVICIO", "Fuera de servicio"),
        ("RESERVADA", "Reservada"),
    ]
    
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20)
    estado = models.CharField(max_length=50, choices=ESTADOS, default="ACTIVA")

    def __str__(self):
        return f"Habitación {self.numero} - {self.area.nombre}"
    
    class Meta:
        verbose_name = "Habitación"
        verbose_name_plural = "Habitaciones"
    