from django import forms
from .models import Turno, TurnoPersonal, Asistencia
from acceso.models import UsuarioRol


class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ["hospital", "nombre", "hora_inicio", "hora_fin"]


class TurnoPersonalForm(forms.ModelForm):
    class Meta:
        model = TurnoPersonal
        fields = ["turno", "medico", "enfermero", "fecha"]


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ["usuario", "hora_entrada", "hora_salida"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Si no es dirección, ocultamos el campo usuario
        if (
            user
            and not UsuarioRol.objects.filter(
                usuario=user, rol__nombre="DIRECCIÓN"
            ).exists()
        ):
            self.fields.pop("usuario")
