from django import forms
from .models import Turno, TurnoPersonal, Asistencia

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['hospital', 'nombre', 'hora_inicio', 'hora_fin']


class TurnoPersonalForm(forms.ModelForm):
    class Meta:
        model = TurnoPersonal
        fields = ['turno', 'medico', 'enfermero', 'fecha']


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['usuario']