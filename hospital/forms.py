from django import forms
from .models import Hospital


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ["nombre", "direccion", "telefono", "correo", "codigo"]
        widgets = {
            "direccion": forms.Textarea(attrs={"rows": 3}),
        }
