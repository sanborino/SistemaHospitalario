from django import forms
from .models import Medico, Enfermero, Personal


class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = [
            "hospital",
            "usuario",
            "nombre",
            "apellido",
            "especialidad",
            "numero_licencia",
            "telefono",
            "correo",
        ]


class EnfermeroForm(forms.ModelForm):
    class Meta:
        model = Enfermero
        fields = [
            "hospital",
            "usuario",
            "nombre",
            "apellido",
            "turno",
        ]


class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = [
            "nombre",
            "email",
            "telefono",
            "area",
            "estado",
            "hospital",
            "usuario",
        ]
