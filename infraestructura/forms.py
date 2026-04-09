from django import forms

from .models import Area, Habitacion

from acceso.access import filtrar_queryset
from hospital.models import Hospital


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["hospital", "nombre", "tipo"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["hospital"], Hospital, user)


class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ["hospital", "area", "numero", "estado"]
        widgets = {
            "numero": forms.TextInput(attrs={"placeholder": "Número o código"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["hospital"], Hospital, user)
            filtrar_queryset(self.fields["area"], Area, user)
