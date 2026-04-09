from acceso.access import filtrar_queryset
from hospital.models import Hospital
from acceso.models import Usuario
from django import forms
from .models import Auditoria


class AuditoriaForm(forms.ModelForm):
    class Meta:
        model = Auditoria
        fields = ["tabla", "operacion", "registro_id", "fecha"]
