from django import forms
from acceso.access import filtrar_queryset
from paciente.models import Paciente
from personal.models import Medico
from hospital.models import Hospital  # asegúrate de importar tu modelo Hospital
from cita.models import Cita


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ["hospital", "paciente", "medico", "fecha", "hora", "motivo", "estado"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora": forms.TimeInput(attrs={"type": "time"}),
            "motivo": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            # 🔑 Centralizamos la lógica en access.py
            filtrar_queryset(self.fields["hospital"], Hospital, user)
            filtrar_queryset(self.fields["paciente"], Paciente, user)
            filtrar_queryset(self.fields["medico"], Medico, user)
