from django import forms
from acceso.access import filtrar_queryset
from hospital.models import Hospital
from paciente.models import Paciente
from infraestructura.models import Cama
from .models import AsignacionCama


class AsignacionCamaForm(forms.ModelForm):
    class Meta:
        model = AsignacionCama
        fields = ["hospital", "paciente", "cama", "fecha_ingreso", "fecha_salida"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["hospital"], Hospital, user)
            filtrar_queryset(self.fields["paciente"], Paciente, user)
            filtrar_queryset(self.fields["cama"], Cama, user)
