from django import forms

from .models import (
    Estudio,
    SolicitudLaboratorio,
    SolicitudDetalle,
    ResultadoLaboratorio,
)


class EstudioForm(forms.ModelForm):
    class Meta:
        model = Estudio
        fields = ["hospital", "nombre", "descripcion", "precio"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }


class SolicitudLaboratorioForm(forms.ModelForm):
    """Formulario para que médico cree solicitud con múltiples estudios."""

    estudios = forms.ModelMultipleChoiceField(
        queryset=Estudio.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Estudios a realizar",
    )

    class Meta:
        model = SolicitudLaboratorio
        fields = ["paciente", "medico"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si es edición, cargar estudios actuales
        if self.instance.pk:
            self.fields["estudios"].initial = (
                self.instance.solicituddetalle_set.values_list("estudio_id", flat=True)
            )

    def save(self, commit=True):
        solicitud = super().save(commit=commit)
        if commit:
            # Guardar estudios seleccionados
            estudios = self.cleaned_data["estudios"]
            # Limpiar detalles previos
            solicitud.solicituddetalle_set.all().delete()
            # Crear nuevos detalles
            for estudio in estudios:
                SolicitudDetalle.objects.create(solicitud=solicitud, estudio=estudio)
        return solicitud


class SolicitudDetalleForm(forms.ModelForm):
    class Meta:
        model = SolicitudDetalle
        fields = ["solicitud", "estudio"]


class ResultadoLaboratorioForm(forms.ModelForm):
    class Meta:
        model = ResultadoLaboratorio
        fields = ["solicitud", "resultados", "firmado_por"]
        widgets = {
            "resultados": forms.Textarea(attrs={"rows": 5}),
        }
