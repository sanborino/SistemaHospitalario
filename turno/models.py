from django.db import models
from personal.models import Medico, Enfermero
from hospital.models import Hospital
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Turno(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return self.nombre


class TurnoPersonal(models.Model):
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True)
    enfermero = models.ForeignKey(
        Enfermero, on_delete=models.SET_NULL, null=True, blank=True
    )
    fecha = models.DateField()

    def __str__(self):
        return f"{self.turno} - {self.fecha}"

    class Meta:
        verbose_name = "Turno Personal"
        verbose_name_plural = "Turno de personal"


class Asistencia(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    hora_entrada = models.TimeField(blank=True, null=True)
    hora_salida = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Asistencia {self.usuario} - {self.fecha}"


@receiver(post_save, sender=Asistencia)
def registrar_auditoria(sender, instance, created, **kwargs):
    if created:
        # Se creó una asistencia → registrar entrada
        print(f"Auditoría: {instance.usuario} entró a las {instance.hora_entrada}")
    else:
        # Se actualizó una asistencia → registrar salida
        if instance.hora_salida:
            print(f"Auditoría: {instance.usuario} salió a las {instance.hora_salida}")
