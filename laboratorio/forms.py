from django import forms

from .models import (
    Estudio,
    SolicitudLaboratorio,
    SolicitudDetalle,
    ResultadoLaboratorio,
)
from acceso.access import filtrar_queryset, visibles_para
from hospital.models import Hospital
from paciente.models import Paciente
from personal.models import Medico


class EstudioForm(forms.ModelForm):
    class Meta:
        model = Estudio
        fields = ["hospital", "nombre", "descripcion", "precio"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["hospital"], Hospital, user)


class SolicitudLaboratorioForm(forms.ModelForm):
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
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            # 🔹 Filtrar pacientes y médicos por hospital
            filtrar_queryset(self.fields["paciente"], Paciente, user)
            filtrar_queryset(self.fields["medico"], Medico, user)

            # 🔹 Si los estudios son globales, no los filtres
            # self.fields["estudios"].queryset = Estudio.objects.all()

            # 🔹 Si los estudios son por hospital, usa el filtro
            filtrar_queryset(self.fields["estudios"], Estudio, user)

        if self.instance.pk:
            self.fields["estudios"].initial = (
                self.instance.solicituddetalle_set.values_list("estudio_id", flat=True)
            )

    def save(self, commit=True):
        solicitud = super().save(commit=commit)
        if commit:
            estudios = self.cleaned_data["estudios"]
            solicitud.solicituddetalle_set.all().delete()
            for estudio in estudios:
                SolicitudDetalle.objects.create(solicitud=solicitud, estudio=estudio)
        return solicitud


class SolicitudDetalleForm(forms.ModelForm):
    class Meta:
        model = SolicitudDetalle
        fields = ["solicitud", "estudio"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["solicitud"], SolicitudLaboratorio, user)
            filtrar_queryset(self.fields["estudio"], Estudio, user)


class ResultadoLaboratorioForm(forms.ModelForm):
    class Meta:
        model = ResultadoLaboratorio
        fields = ["solicitud", "resultados", "firmado_por"]
        widgets = {
            "resultados": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            # Filtrar solicitudes visibles y que no tengan resultado aún
            qs_solicitudes = visibles_para(SolicitudLaboratorio, user).exclude(
                resultadolaboratorio__isnull=False
            )
            self.fields["solicitud"].queryset = qs_solicitudes
            filtrar_queryset(self.fields["firmado_por"], Medico, user)
