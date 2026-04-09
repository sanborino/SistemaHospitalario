from django import forms
from .models import Insumo, MovimientoInventario
from acceso.access import filtrar_queryset
from hospital.models import Hospital


class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ["hospital", "nombre", "descripcion", "stock", "unidad"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["hospital"], Hospital, user)


class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ["insumo", "tipo", "cantidad"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["insumo"], Insumo, user)
