from django import forms
from .models import Medicamento, Receta, RecetaDetalle, Dispensacion
from acceso.models import UsuarioRol, UsuarioHospital
from paciente.models import Paciente
from personal.models import Medico
from acceso.access import filtrar_queryset
from hospital.models import Hospital


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["hospital"], Hospital, user)

            # Pre-seleccionar el hospital del usuario para creación
            if not self.instance.pk:  # Solo para creación
                hospital_usuario = user.usuariohospital_set.first()
                if hospital_usuario:
                    self.fields["hospital"].initial = hospital_usuario.hospital

                    # Para roles no globales, hacer el campo readonly
                    if not (
                        user.is_superuser
                        or user.usuariorol_set.filter(
                            rol__nombre__in=["DIRECCIÓN", "SISTEMAS"]
                        ).exists()
                    ):
                        self.fields["hospital"].widget.attrs["readonly"] = True


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ["paciente", "medico", "indicaciones"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["paciente"], Paciente, user)
            filtrar_queryset(self.fields["medico"], Medico, user)


class RecetaDetalleForm(forms.ModelForm):
    class Meta:
        model = RecetaDetalle
        fields = ["medicamento", "cantidad"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["medicamento"], Medicamento, user)


class DispensacionForm(forms.ModelForm):
    class Meta:
        model = Dispensacion
        fields = [
            "observaciones"
        ]  # Quitamos receta y entregado_por, se asignan en la vista

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
