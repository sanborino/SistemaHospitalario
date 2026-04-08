from django import forms

from .models import Insumo, MovimientoInventario


class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ["hospital", "nombre", "descripcion", "stock", "unidad"]
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }


class MovimientoInventarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ["insumo", "tipo", "cantidad"]
