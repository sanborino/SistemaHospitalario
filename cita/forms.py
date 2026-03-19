from django import forms
from .models import Cita

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ["hospital", "paciente", "medico", "fecha", "hora", "motivo", "estado"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora": forms.TimeInput(attrs={"type": "time"}),
            "motivo": forms.Textarea(attrs={"rows": 3}),
        }