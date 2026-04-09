from django.db import models
from hospital.models import Hospital
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class Rol(models.Model):

    NOMBRES = [
        ("MÉDICO", "Médico"),
        ("ENFERMERO", "Enfermero"),
        ("LABORATORIO", "Laboratorio"),
        ("FARMACIA", "Farmacia"),
        ("ADMINISTRACIÓN", "Administración"),
        ("URGENCIAS", "Urgencias"),
        ("MANTENIMIENTO", "Mantenimiento"),
        ("SISTEMAS", "Sistemas"),
        ("DIRECCIÓN", "Dirección"),
    ]

    nombre = models.CharField(max_length=70, choices=NOMBRES, default="MÉDICO")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"


class Permiso(models.Model):

    PERMISOS = [
        ("PACIENTES", "Pacientes"),
        ("LABORATORIO", "Laboratorio"),
        ("HISTORIAL CLINICO", "Historial Clinico"),
        ("INVENTARIOS", "Inventarios"),
        ("FACTURACIÓN", "Facturación"),
        ("URGENCIAS", "Urgencias"),
        ("HOSPITALIZACIÓN", "Hospitalización"),
        ("INFRAESTRUCTURA", "Ingfraestructura"),
        ("ADMINISTRACIÓN", "Administración"),
        ("TURNOS", "Turnos"),
        ("SISTEMAS", "Sisitemas"),
    ]

    nombre = models.CharField(max_length=100, choices=PERMISOS, default="PACIENTES")
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class UsuarioManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("El usuario debe tener un nombre de usuario")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):

    ESTADOS = [
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
        ("SUSPENDIDO", "Suspendido"),
        ("ELIMINADO", "Eliminado"),
    ]

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="ACTIVO")

    # Campos requeridos por Django Admin
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


class UsuarioRol(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Usuario y Rol"
        verbose_name_plural = "Usuarios y Roles"
        unique_together = ("usuario", "rol")


class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Rol y permiso"
        verbose_name_plural = "Roles y permisos"


class UsuarioHospital(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Usuario de Hospital"
        verbose_name_plural = "Usuarios de Hospitales"
