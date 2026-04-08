from django import forms
from acceso.models import UsuarioRol, UsuarioHospital
from .models import Urgencia, AtencionUrgencia, AltaUrgencia


class UrgenciaForm(forms.ModelForm):
    class Meta:
        model = Urgencia
        fields = ["hospital", "paciente", "nivel_triaje", "motivo", "estado"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if (
            user
            and not UsuarioRol.objects.filter(
                usuario=user, rol__nombre="DIRECCIÓN"
            ).exists()
        ):
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if hospital_usuario:
                self.fields["hospital"].initial = hospital_usuario.hospital
            self.fields["hospital"].widget = forms.HiddenInput()


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
