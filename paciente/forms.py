from django import forms
from .models import Paciente, Hospital
from acceso.access import filtrar_queryset


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
            # 🔑 Centralizamos la lógica en access.py
            filtrar_queryset(self.fields["hospital"], Hospital, user)
