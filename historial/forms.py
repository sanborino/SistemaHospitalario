from django import forms
from .models import HistorialClinico
from acceso.models import UsuarioRol, UsuarioHospital


class HistorialClinicoForm(forms.ModelForm):
    class Meta:
        model = HistorialClinico
        fields = [
            "hospital",
            "paciente",
            "medico",
            "cita",
            "diagnostico",
            "tratamiento",
            "notas",
        ]
        widgets = {
            "hospital": forms.Select(attrs={"class": "form-select"}),
            "paciente": forms.Select(attrs={"class": "form-select"}),
            "medico": forms.Select(attrs={"class": "form-select"}),
            "diagnostico": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "tratamiento": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "notas": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # recibimos el usuario desde la vista
        super().__init__(*args, **kwargs)

        if user:
            # Si es director → puede elegir hospital
            if UsuarioRol.objects.filter(
                usuario=user, rol__nombre="DIRECCIÓN"
            ).exists():
                self.fields["hospital"].queryset = HistorialClinico._meta.get_field(
                    "hospital"
                ).related_model.objects.all()
            else:
                # Si no es director → hospital fijo y campo oculto
                hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
                if hospital_usuario:
                    self.fields["hospital"].initial = hospital_usuario.hospital
                self.fields["hospital"].widget = forms.HiddenInput()
