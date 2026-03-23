from django import forms

from .models import Urgencia, AtencionUrgencia, AltaUrgencia


class UrgenciaForm(forms.ModelForm):
    class Meta:
        model = Urgencia
        fields = ["hospital", "paciente", "nivel_triaje", "motivo", "estado"]
        widgets = {
            "motivo": forms.Textarea(attrs={"rows": 4}),
        }


class AtencionUrgenciaForm(forms.ModelForm):
    class Meta:
        model = AtencionUrgencia
        fields = ["urgencia", "medico", "notas"]
        widgets = {
            "notas": forms.Textarea(attrs={"rows": 4}),
        }


class AltaUrgenciaForm(forms.ModelForm):
    class Meta:
        model = AltaUrgencia
        fields = ["urgencia", "diagnostico_final", "recomendaciones"]
        widgets = {
            "diagnostico_final": forms.Textarea(attrs={"rows": 4}),
            "recomendaciones": forms.Textarea(attrs={"rows": 4}),
        }
