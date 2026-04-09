from django import forms
from acceso.models import UsuarioRol, UsuarioHospital
from .models import Urgencia, AtencionUrgencia, AltaUrgencia
from acceso.access import filtrar_queryset
from hospital.models import Hospital
from paciente.models import Paciente
from personal.models import Medico


class UrgenciaForm(forms.ModelForm):
    class Meta:
        model = Urgencia
        fields = ["hospital", "paciente", "nivel_triaje", "motivo", "estado"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            filtrar_queryset(self.fields["hospital"], Hospital, user)
            filtrar_queryset(self.fields["paciente"], Paciente, user)


class AtencionUrgenciaForm(forms.ModelForm):
    class Meta:
        model = AtencionUrgencia
        fields = ["urgencia", "medico", "notas"]
        widgets = {
            "notas": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            filtrar_queryset(self.fields["urgencia"], Urgencia, user)
            self.fields["urgencia"].queryset = self.fields["urgencia"].queryset.exclude(
                estado__in=["EN_ATENCION", "DADO_DE_ALTA", "CERRADO"]
            )
            filtrar_queryset(self.fields["medico"], Medico, user)


class AltaUrgenciaForm(forms.ModelForm):
    class Meta:
        model = AltaUrgencia
        fields = ["urgencia", "diagnostico_final", "recomendaciones"]
        widgets = {
            "diagnostico_final": forms.Textarea(attrs={"rows": 4}),
            "recomendaciones": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            filtrar_queryset(self.fields["urgencia"], Urgencia, user)
