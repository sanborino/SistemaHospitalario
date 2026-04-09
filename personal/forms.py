from django import forms
from .models import Medico, Enfermero, Personal
from acceso.access import filtrar_queryset
from hospital.models import Hospital
from infraestructura.models import Area


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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["hospital"], Hospital, user)


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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["hospital"], Hospital, user)


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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["hospital"], Hospital, user)
            filtrar_queryset(self.fields["area"], Area, user)
