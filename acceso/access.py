# access.py
from django.core.exceptions import PermissionDenied


# access.py
ROLES_GLOBAL = ["DIRECCIÓN", "SISTEMAS"]
ROLES_HOSPITAL = ["MÉDICO", "ENFERMERO", "FARMACIA", "LABORATORIO", "MANTENIMIENTO"]

CAMPOS_HOSPITAL = {
    "Paciente": "hospital",
    "Medico": "usuario__usuariohospital__hospital",
    "Estudio": "hospital",
    "Receta": "paciente__hospital",
    "Personal": "hospital",
    "SolicitudLaboratorio": "paciente__hospital",
    "ResultadoLaboratorio": "solicitud__paciente__hospital",
    "Factura": "hospital",
    "FacturaDetalle": "factura__hospital",
    "HistorialClinico": "hospital",
    "Cita": "hospital",
    "Medicamento": "hospital",
    "Urgencia": "hospital",
    "AtencionUrgencia": "urgencia__hospital",
    "AltaUrgencia": "urgencia__hospital",
    "Area": "hospital",
    "Insumo": "hospital",
    "MovimientoInventario": "insumo__hospital",
    "Cama": "habitacion__hospital",
    "Habitacion": "hospital",
    "AsignacionCama": "cama__habitacion__hospital",
}


def visibles_para(model_cls, user):
    qs = model_cls.objects.all()

    if (
        user.is_superuser
        or user.usuariorol_set.filter(rol__nombre__in=ROLES_GLOBAL).exists()
    ):
        return qs

    if user.usuariorol_set.filter(rol__nombre__in=ROLES_HOSPITAL).exists():
        hospital_ids = user.usuariohospital_set.values_list("hospital_id", flat=True)
        campo = CAMPOS_HOSPITAL.get(model_cls.__name__)
        if campo:
            return qs.filter(**{f"{campo}__in": hospital_ids})
        elif model_cls.__name__ == "Hospital":
            return qs.filter(id__in=hospital_ids)

    if model_cls.__name__ == "Asistencia":
        return qs.filter(usuario=user)

    return qs.none()


def filtrar_queryset(field, model_cls, user):
    if (
        user.is_superuser
        or user.usuariorol_set.filter(rol__nombre__in=ROLES_GLOBAL).exists()
    ):
        field.queryset = model_cls.objects.all()
        return

    hospital_usuario = user.usuariohospital_set.first()
    if not hospital_usuario:
        field.queryset = model_cls.objects.none()
        return

    campo = CAMPOS_HOSPITAL.get(model_cls.__name__)
    if campo:
        field.queryset = model_cls.objects.filter(**{campo: hospital_usuario.hospital})
    else:
        field.queryset = model_cls.objects.none()


# access.py
def filtrar_queryset(field, model_cls, user):
    """
    Ajusta el queryset de un campo de formulario según el usuario y el modelo.
    """
    # Roles con acceso global
    if (
        user.is_superuser
        or user.usuariorol_set.filter(
            rol__nombre__in=["DIRECCIÓN", "SISTEMAS"]
        ).exists()
    ):
        field.queryset = model_cls.objects.all()
        return

    hospital_usuario = user.usuariohospital_set.first()
    if not hospital_usuario:
        field.queryset = model_cls.objects.none()
        return

    hospital_obj = hospital_usuario.hospital

    # 🔹 Diccionario de mapeo: modelo → campo hospital
    campos_por_modelo = {
        "Paciente": "hospital",
        "Medico": "usuario__usuariohospital__hospital",
        "Estudio": "hospital",
        "Receta": "paciente__hospital",
        "Personal": "hospital",
        "SolicitudLaboratorio": "paciente__hospital",
        "ResultadoLaboratorio": "solicitud__paciente__hospital",
        "Factura": "hospital",
        "FacturaDetalle": "factura__hospital",
        "HistorialClinico": "hospital",
        "Cita": "hospital",
        "Medicamento": "hospital",
        "Urgencia": "hospital",
        "AtencionUrgencia": "urgencia__hospital",
        "AltaUrgencia": "urgencia__hospital",
        "Area": "hospital",
        "Insumo": "hospital",
        "MovimientoInventario": "insumo__hospital",
        "Cama": "habitacion__hospital",
        "Habitacion": "hospital",
        "AsignacionCama": "cama__habitacion__hospital",
    }

    campo = campos_por_modelo.get(model_cls.__name__)

    if campo:
        try:
            field.queryset = model_cls.objects.filter(**{campo: hospital_obj})
        except Exception:
            field.queryset = model_cls.objects.none()
    elif model_cls.__name__ == "Hospital":
        # Para Hospital, filtrar por los hospitales del usuario
        hospital_ids = user.usuariohospital_set.values_list("hospital_id", flat=True)
        field.queryset = model_cls.objects.filter(id__in=hospital_ids)
    else:
        field.queryset = model_cls.objects.none()


class HospitalAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # Permitir acceso si tiene rol global (DIRECCIÓN o SISTEMAS)
        if request.user.usuariorol_set.filter(
            rol__nombre__in=["DIRECCIÓN", "SISTEMAS"]
        ).exists():
            return super().dispatch(request, *args, **kwargs)

        # 🔹 Permitir siempre acceso a Asistencia
        if self.model.__name__ == "Asistencia":
            return super().dispatch(request, *args, **kwargs)

        # Verificar si el usuario tiene acceso a al menos un hospital
        if request.user.usuariohospital_set.exists():
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("No tienes acceso a este hospital")


"""
APLICAR EN VISTAS
from .access import visibles_para
from .models import Factura

def lista_facturas(request):
    facturas = visibles_para(Factura, request.user)
    return render(request, "facturas/lista.html", {"facturas": facturas})
    
    
APLICAR EN CLASES
from django.views.generic import ListView
from .access import HospitalAccessMixin
from .models import Paciente

class PacienteListView(HospitalAccessMixin, ListView):
    model = Paciente
    template_name = "pacientes/lista.html"

APLICAR EN FORMULARIOS
from django import forms
from .models import Factura, Hospital
from .access import visibles_para

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ["paciente", "hospital", "total"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["hospital"].queryset = visibles_para(Hospital, user)
        
EN LA VISTA:

form = FacturaForm(request.POST or None, user=request.user)

APLICAR EN EL ADMIN
from django.contrib import admin
from .models import Factura
from .access import visibles_para

class FacturaAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return visibles_para(Factura, request.user)

admin.site.register(Factura, FacturaAdmin)

APIs (DRF)
from rest_framework import viewsets
from .models import Medicamento
from .access import visibles_para
from .serializers import MedicamentoSerializer

class MedicamentoViewSet(viewsets.ModelViewSet):
    serializer_class = MedicamentoSerializer

    def get_queryset(self):
        Return visibles_para(Medicamento, self.request.user)

"""
