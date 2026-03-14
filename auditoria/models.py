from django.db import models

# Create your models here.

class Auditoria(models.Model):
    tabla = models.CharField(max_length=100)
    operacion = models.CharField(max_length=20)
    registro_id = models.IntegerField(null=True, blank=True)
    fecha = models.DateTimeField()

    class Meta:
        db_table = 'auditoria'
        verbose_name = 'Auditoría'
        verbose_name_plural = 'Auditorías'

    def __str__(self):
        return f"{self.tabla} - {self.operacion} - {self.registro_id}"