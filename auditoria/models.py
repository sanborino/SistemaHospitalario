from django.db import models
from django.utils import timezone
from django.db.models import Value
from django.db.models.functions import Now

# Create your models here.


class Auditoria(models.Model):
    tabla = models.CharField(max_length=100)
    operacion = models.CharField(max_length=20)
    registro_id = models.IntegerField(null=True, blank=True)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "auditoria"
        verbose_name = "Auditoría"
        verbose_name_plural = "Auditorías"

    def __str__(self):
        return f"{self.tabla} - {self.operacion} - {self.registro_id}"
