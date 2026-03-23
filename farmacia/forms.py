from django import forms
from .models import Medicamento, Receta, RecetaDetalle, Dispensacion

class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = '__all__'


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = '__all__'


class RecetaDetalleForm(forms.ModelForm):
    class Meta:
        model = RecetaDetalle
        fields = '__all__'


class DispensacionForm(forms.ModelForm):
    class Meta:
        model = Dispensacion
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo recetas NO surtidas
        self.fields["receta"].queryset = Receta.objects.filter(dispensacion__isnull=True)