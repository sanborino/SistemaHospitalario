from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuario, Rol, Permiso, UsuarioRol, RolPermiso, UsuarioHospital
from acceso.access import filtrar_queryset
from hospital.models import Hospital
from django.contrib.auth.hashers import make_password


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput, label="Confirmar contraseña"
    )

    class Meta:
        model = Usuario
        fields = ["username", "email", "password", "password_confirm"]
        labels = {
            "username": "Usuario",
            "email": "Correo electrónico",
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password_confirm")

        if p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password"])  # encripta la contraseña
        usuario.estado = "ACTIVO"  # estado inicial del usuario
        if commit:
            usuario.save()
        return usuario


class UsuarioRolForm(forms.ModelForm):
    class Meta:
        model = UsuarioRol
        fields = ["usuario", "rol"]
        labels = {
            "usuario": "Usuario",
            "rol": "Rol",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["usuario"], Usuario, user)
            # Los roles son globales, no se filtran por hospital

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get("usuario")
        rol = cleaned_data.get("rol")
        if usuario and rol:
            qs = UsuarioRol.objects.filter(usuario=usuario, rol=rol)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Este usuario ya tiene asignado ese rol.")
        return cleaned_data


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ["nombre"]
        labels = {
            "nombre": "Rol",
        }


class PermisoForm(forms.ModelForm):
    class Meta:
        model = Permiso
        fields = ["nombre", "descripcion"]
        labels = {
            "nombre": "Permiso",
            "descripcion": "Descripción",
        }


class RolPermisoForm(forms.ModelForm):
    class Meta:
        model = RolPermiso
        fields = ["rol", "permiso"]
        labels = {
            "rol": "Rol",
            "permiso": "Permiso",
        }


class UsuarioHospitalForm(forms.ModelForm):
    class Meta:
        model = UsuarioHospital
        fields = ["usuario", "hospital"]
        labels = {
            "usuario": "Usuario",
            "hospital": "Hospital",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["usuario"], Usuario, user)
            filtrar_queryset(self.fields["hospital"], Hospital, user)
