from acceso.access import filtrar_queryset
from hospital.models import Hospital
from paciente.models import Paciente
from personal.models import Medico
from cita.models import Cita
from django import forms
from .models import HistorialClinico


class HistorialClinicoForm(forms.ModelForm):
    class Meta:
        model = HistorialClinico
        fields = [
            "hospital",
            "paciente",
            "medico",
            "cita",
            "diagnostico",
            "tratamiento",
            "notas",
        ]
        widgets = {
            "hospital": forms.Select(attrs={"class": "form-select"}),
            "paciente": forms.Select(attrs={"class": "form-select"}),
            "medico": forms.Select(attrs={"class": "form-select"}),
            "diagnostico": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "tratamiento": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "notas": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["hospital"], Hospital, user)
            filtrar_queryset(self.fields["paciente"], Paciente, user)
            filtrar_queryset(self.fields["medico"], Medico, user)
            # Para cita, si es necesario
            if "cita" in self.fields:
                filtrar_queryset(self.fields["cita"], Cita, user)

            # Pre-seleccionar el hospital del usuario para creación
            if not self.instance.pk:  # Solo para creación
                hospital_usuario = user.usuariohospital_set.first()
                if hospital_usuario:
                    self.fields["hospital"].initial = hospital_usuario.hospital

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # recibimos el usuario desde la vista
        super().__init__(*args, **kwargs)

        if user:
            # 🔑 Centralizamos la lógica en access.py
            filtrar_queryset(self.fields["hospital"], Hospital, user)
            filtrar_queryset(self.fields["paciente"], Paciente, user)
            filtrar_queryset(self.fields["medico"], Medico, user)
            filtrar_queryset(self.fields["cita"], Cita, user)
