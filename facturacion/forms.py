from django import forms
from .models import Factura, FacturaDetalle, Pago
from acceso.models import UsuarioRol, UsuarioHospital


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ["hospital", "paciente", "total", "estado"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Si no es director, ocultamos el campo hospital
        if (
            user
            and not UsuarioRol.objects.filter(
                usuario=user, rol__nombre="DIRECCIÓN"
            ).exists()
        ):
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if hospital_usuario:
                self.fields["hospital"].initial = hospital_usuario.hospital
            self.fields["hospital"].widget = forms.HiddenInput()


class FacturaDetalleForm(forms.ModelForm):
    class Meta:
        model = FacturaDetalle
        fields = ["factura", "descripcion", "cantidad", "precio_unitario"]


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ["factura", "monto", "metodo"]
