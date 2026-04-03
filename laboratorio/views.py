from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from decimal import Decimal
from facturacion.models import Cargo
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from personal.models import Medico
from paciente.models import Paciente
from .models import (
    Estudio,
    SolicitudLaboratorio,
    SolicitudDetalle,
    ResultadoLaboratorio,
)
from .forms import (
    EstudioForm,
    SolicitudLaboratorioForm,
    ResultadoLaboratorioForm,
)
from django.contrib.auth.decorators import login_required

@login_required
def crear_factura_solicitud(solicitud):
    """Crea automaticamente una Factura + FacturaDetalles para la solicitud."""
    from facturacion.models import Factura, FacturaDetalle

    # Obtener todos los estudios de la solicitud
    detalles = solicitud.solicituddetalle_set.all()

    if not detalles.exists():
        return None

    # Calcular total
    total = Decimal("0.00")
    for detalle in detalles:
        total += detalle.estudio.precio

    # Crear factura
    factura = Factura.objects.create(
        hospital=solicitud.medico.hospital,  # Hospital del médico
        paciente=solicitud.paciente,
        solicitud=solicitud,
        total=total,
        estado="PENDIENTE",
        origen_estudio=True,
    )

    # Crear detalles de factura
    for detalle in detalles:
        FacturaDetalle.objects.create(
            factura=factura,
            descripcion=f"Estudio: {detalle.estudio.nombre}",
            cantidad=1,
            precio_unitario=detalle.estudio.precio,
        )

    return factura


# CRUD Estudio


class EstudioCreateView(LoginRequiredMixin, CreateView):
    model = Estudio
    form_class = EstudioForm
    template_name = "laboratorio/estudio_formulario.html"

    def get_success_url(self):
        return reverse_lazy(
            "laboratorio:detalle_estudio", kwargs={"pk": self.object.pk}
        )


class EstudioUpdateView(LoginRequiredMixin, UpdateView):
    model = Estudio
    form_class = EstudioForm
    template_name = "laboratorio/estudio_formulario.html"

    def get_success_url(self):
        return reverse_lazy(
            "laboratorio:detalle_estudio", kwargs={"pk": self.object.pk}
        )


class EstudioDeleteView(LoginRequiredMixin, DeleteView):
    model = Estudio
    template_name = "laboratorio/estudio_confirmar_eliminar.html"
    success_url = reverse_lazy("laboratorio:lista_estudio")


class EstudioListView(LoginRequiredMixin, ListView):
    model = Estudio
    template_name = "laboratorio/estudio_lista.html"
    context_object_name = "estudios"
    paginate_by = 10
    ordering = ["nombre"]


class EstudioDetailView(LoginRequiredMixin, DetailView):
    model = Estudio
    template_name = "laboratorio/estudio_detalle.html"
    context_object_name = "estudio"


class EstudioUpdateView(LoginRequiredMixin, UpdateView):
    model = Estudio
    form_class = EstudioForm
    template_name = "laboratorio/estudio_formulario.html"

    def get_success_url(self):
        return reverse_lazy(
            "laboratorio:detalle_estudio", kwargs={"pk": self.object.pk}
        )


# CRUD SolicitudLaboratorio
class SolicitudListView(LoginRequiredMixin, ListView):
    model = SolicitudLaboratorio
    template_name = "laboratorio/solicitud_lista.html"
    context_object_name = "solicitudes"
    paginate_by = 10
    ordering = ["-fecha"]

    def get_queryset(self):
        queryset = super().get_queryset().select_related("paciente", "medico")

        # --- Filtros opcionales ---
        paciente_id = self.request.GET.get("paciente")
        medico_id = self.request.GET.get("medico")
        estado = self.request.GET.get("estado")

        if paciente_id:
            queryset = queryset.filter(paciente_id=paciente_id)

        if medico_id:
            queryset = queryset.filter(medico_id=medico_id)

        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Para filtros en el template
        context["pacientes"] = Paciente.objects.all().order_by("apellido", "nombre")
        context["medicos"] = Medico.objects.all().order_by("apellido", "nombre")

        # Mantener valores seleccionados
        context["filtro_paciente"] = self.request.GET.get("paciente", "")
        context["filtro_medico"] = self.request.GET.get("medico", "")
        context["filtro_estado"] = self.request.GET.get("estado", "")

        return context


class SolicitudCreateView(LoginRequiredMixin, CreateView):
    model = SolicitudLaboratorio
    form_class = SolicitudLaboratorioForm
    template_name = "laboratorio/solicitud_formulario.html"

    def form_valid(self, form):
        # Verificar que el usuario tenga al menos un médico asociado
        medico_qs = Medico.objects.filter(usuario=self.request.user)
        if not medico_qs.exists():
            raise PermissionDenied("Solo los médicos pueden crear solicitudes de laboratorio.")

        # Tomar el primer médico asociado (ajusta la lógica si necesitas otro criterio)
        medico = medico_qs.first()

        # Crear la solicitud y asignar el médico
        solicitud = form.save(commit=False)
        solicitud.medico = medico
        solicitud.save()

        # Crear factura automáticamente
        crear_factura_solicitud(solicitud)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "laboratorio:detalle_solicitud", kwargs={"pk": self.object.pk}
        )


class SolicitudUpdateView(LoginRequiredMixin, UpdateView):
    model = SolicitudLaboratorio
    form_class = SolicitudLaboratorioForm
    template_name = "laboratorio/solicitud_formulario.html"

    def get_success_url(self):
        return reverse_lazy(
            "laboratorio:detalle_solicitud", kwargs={"pk": self.object.pk}
        )


class SolicitudDeleteView(LoginRequiredMixin, DeleteView):
    model = SolicitudLaboratorio
    template_name = "laboratorio/solicitud_confirmar_eliminar.html"
    success_url = reverse_lazy("laboratorio:lista_solicitud")
    


class SolicitudDetailView(LoginRequiredMixin, DetailView):
    model = SolicitudLaboratorio
    template_name = "laboratorio/solicitud_detalle.html"
    context_object_name = "solicitud"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar los estudios asociados a esta solicitud
        context["estudios"] = SolicitudDetalle.objects.filter(solicitud=self.object)
        return context

# CRUD ResultadoLaboratorio


class ResultadoListView(LoginRequiredMixin, ListView):
    model = ResultadoLaboratorio
    template_name = "laboratorio/resultado_lista.html"
    context_object_name = "resultados"
    paginate_by = 10
    ordering = ["-fecha"]

    def get_queryset(self):
        queryset = super().get_queryset().select_related("solicitud", "firmado_por")

        # Obtener parámetros GET
        paciente = self.request.GET.get("paciente")
        estado = self.request.GET.get("estado")
        fecha = self.request.GET.get("fecha")

        # Filtro por paciente (nombre o apellido)
        if paciente:
            queryset = queryset.filter(
                Q(solicitud__paciente__nombre__icontains=paciente)
                | Q(solicitud__paciente__apellido__icontains=paciente)
            )

        # Filtro por estado de la solicitud
        if estado and estado != "todos":
            queryset = queryset.filter(solicitud__estado=estado)

        # Filtro por fecha exacta del resultado
        if fecha:
            queryset = queryset.filter(fecha=fecha)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Mantener valores seleccionados en el template
        context["paciente_busqueda"] = self.request.GET.get("paciente", "")
        context["estado_seleccionado"] = self.request.GET.get("estado", "todos")
        context["fecha_busqueda"] = self.request.GET.get("fecha", "")

        # Opciones de estado
        context["estados"] = [
            ("todos", "Todos"),
            ("pendiente", "Pendiente"),
            ("finalizado", "Finalizado"),
        ]

        return context


class ResultadoDetailView(LoginRequiredMixin, DetailView):
    model = ResultadoLaboratorio
    template_name = "laboratorio/resultado_detalle.html"
    context_object_name = "resultado"


class ResultadoCreateView(LoginRequiredMixin, CreateView):
    model = ResultadoLaboratorio
    form_class = ResultadoLaboratorioForm
    template_name = "laboratorio/resultado_formulario.html"

    def form_valid(self, form):
        resultado = form.save()
        solicitud = resultado.solicitud
        solicitud.estado = SolicitudLaboratorio.ESTADO_FINALIZADO
        solicitud.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "laboratorio:detalle_resultado", kwargs={"pk": self.object.pk}
        )


class ResultadoUpdateView(LoginRequiredMixin, UpdateView):
    model = ResultadoLaboratorio
    form_class = ResultadoLaboratorioForm
    template_name = "laboratorio/resultado_formulario.html"

    def get_success_url(self):
        return reverse_lazy(
            "laboratorio:detalle_resultado", kwargs={"pk": self.object.pk}
        )


class ResultadoDeleteView(LoginRequiredMixin, DeleteView):
    model = ResultadoLaboratorio
    template_name = "laboratorio/resultado_confirmar_eliminar.html"
    success_url = reverse_lazy("laboratorio:lista_resultado")

@login_required
def finalizar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudLaboratorio, pk=id)

    for det in solicitud.solicituddetalle_set.all():
        Cargo.objects.create(
            paciente=solicitud.paciente,
            descripcion=f"Estudio: {det.estudio.nombre}",
            cantidad=1,
            precio_unitario=det.estudio.precio,
            laboratorio=solicitud,
        )

    solicitud.estado = "finalizado"
    solicitud.save()

    messages.success(request, "Solicitud finalizada y cargos generados.")
    return redirect("laboratorio:solicitud_detalle", id)
