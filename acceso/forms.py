from django import forms
from django.contrib.auth.hashers import make_password
from .models import Usuario, Rol, Permiso, UsuarioRol, RolPermiso, UsuarioHospital


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
        usuario.set_password(self.cleaned_data["password"])
        usuario.estado = "ACTIVO"
        if commit:
            usuario.save()
        return usuario


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


class UsuarioRolForm(forms.ModelForm):
    class Meta:
        model = UsuarioRol
        fields = ["usuario", "rol"]
        labels = {
            "usuario": "Usuario",
            "rol": "Rol",
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
