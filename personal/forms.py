from django import forms
from .models import Medico, Enfermero

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = [
            'hospital',
            'usuario',
            'nombre',
            'apellido',
            'especialidad',
            'numero_licencia',
            'telefono',
            'correo',
        ]


class EnfermeroForm(forms.ModelForm):
    class Meta:
        model = Enfermero
        fields = [
            'usuario',
            'nombre',
            'apellido',
            'turno',
        ]