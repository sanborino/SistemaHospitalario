from django import forms
from .models import Turno, TurnoPersonal, Asistencia
from acceso.models import UsuarioRol, Usuario
from personal.models import Medico, Enfermero
from acceso.access import filtrar_queryset
from hospital.models import Hospital


class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ["hospital", "nombre", "hora_inicio", "hora_fin"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["hospital"], Hospital, user)


class TurnoPersonalForm(forms.ModelForm):
    class Meta:
        model = TurnoPersonal
        fields = ["turno", "medico", "enfermero", "fecha"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["turno"], Turno, user)
            filtrar_queryset(self.fields["medico"], Medico, user)
            filtrar_queryset(self.fields["enfermero"], Enfermero, user)


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ["usuario", "hora_entrada", "hora_salida"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            filtrar_queryset(self.fields["usuario"], Usuario, user)

            # Si no es dirección, ocultamos el campo usuario
            if not UsuarioRol.objects.filter(
                usuario=user, rol__nombre="DIRECCIÓN"
            ).exists():
                self.fields.pop("usuario")
