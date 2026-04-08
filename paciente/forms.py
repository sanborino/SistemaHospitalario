from django import forms
from .models import Paciente, Hospital
from acceso.models import UsuarioRol, UsuarioHospital


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "hospital",
            "nombre",
            "apellido",
            "fecha_nacimiento",
            "sexo",
            "direccion",
            "telefono",
            "contacto_emergencia",
            "tipo_sangre",
            "alergias",
        ]
        widgets = {
            "hospital": forms.Select(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "apellido": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "sexo": forms.Select(
                attrs={"class": "form-select"},
                choices=[
                    ("MASCULINO", "Masculino"),
                    ("FEMENINO", "Femenino"),
                    ("OTRO", "Otro"),
                ],
            ),
            "direccion": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "contacto_emergencia": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_sangre": forms.Select(attrs={"class": "form-select"}),
            "alergias": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            # Si es director → puede elegir hospital
            if UsuarioRol.objects.filter(
                usuario=user, rol__nombre="DIRECCIÓN"
            ).exists():
                self.fields["hospital"].queryset = Hospital.objects.all()
            else:
                # Si no es director → hospital fijo y campo oculto
                hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
                if hospital_usuario:
                    self.fields["hospital"].initial = hospital_usuario.hospital
                self.fields["hospital"].widget = forms.HiddenInput()
