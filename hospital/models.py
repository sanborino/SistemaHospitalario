from django.db import models

# Create your models here.

class Hospital(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    codigo = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitales"