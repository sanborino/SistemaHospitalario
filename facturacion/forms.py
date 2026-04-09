from django import forms
from .models import Factura, FacturaDetalle, Pago
from hospital.models import Hospital
from paciente.models import Paciente

from acceso.access import filtrar_queryset


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ["hospital", "paciente", "total", "estado"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            # 🔑 Centralizamos la lógica en access.py
            filtrar_queryset(self.fields["hospital"], Hospital, user)
            filtrar_queryset(self.fields["paciente"], Paciente, user)


class FacturaDetalleForm(forms.ModelForm):
    class Meta:
        model = FacturaDetalle
        fields = ["factura", "descripcion", "cantidad", "precio_unitario"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["factura"], Factura, user)


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ["factura", "monto", "metodo"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            filtrar_queryset(self.fields["factura"], Factura, user)
