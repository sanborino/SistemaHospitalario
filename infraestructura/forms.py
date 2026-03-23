from django import forms

from .models import Area, Habitacion


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["hospital", "nombre", "tipo"]


class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ["hospital", "area", "numero", "estado"]

        widgets = {
            "numero": forms.TextInput(attrs={"placeholder": "Número o código"}),
        }