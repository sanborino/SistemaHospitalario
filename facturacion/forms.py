from django import forms
from .models import Factura, FacturaDetalle, Pago

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ["hospital", "paciente", "total", "estado"]


class FacturaDetalleForm(forms.ModelForm):
    class Meta:
        model = FacturaDetalle
        fields = ["factura", "descripcion", "cantidad", "precio_unitario"]


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ["factura", "monto", "metodo"]