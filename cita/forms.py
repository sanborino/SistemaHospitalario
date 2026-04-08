from django import forms
from .models import Cita
from acceso.models import UsuarioRol, UsuarioHospital


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ["hospital", "paciente", "medico", "fecha", "hora", "motivo", "estado"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "hora": forms.TimeInput(attrs={"type": "time"}),
            "motivo": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # 👈 extraer el usuario si viene de la vista
        super().__init__(*args, **kwargs)

        if user:
            # Si no es director → ocultar hospital y fijar hospital asignado
            if not UsuarioRol.objects.filter(
                usuario=user, rol__nombre="DIRECCIÓN"
            ).exists():
                hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
                if hospital_usuario:
                    self.fields["hospital"].initial = hospital_usuario.hospital
                # ocultar el campo hospital en el formulario
                self.fields["hospital"].widget = forms.HiddenInput()
