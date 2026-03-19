from django import forms
from .models import HistorialClinico

class HistorialClinicoForm(forms.ModelForm):
    class Meta:
        model = HistorialClinico
        fields = ["hospital", "paciente", "medico", "cita","diagnostico", "tratamiento", "notas"]
        widgets = {
            "hospital": forms.Select(attrs={"class": "form-select"}),
            "paciente": forms.Select(attrs={"class": "form-select"}),
            "medico": forms.Select(attrs={"class": "form-select"}),
            "diagnostico": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "tratamiento": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "notas": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }