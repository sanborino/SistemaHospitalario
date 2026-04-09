from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Paciente
from .forms import PacienteForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from hospitalizacion.models import AsignacionCama
from acceso.mixins import PermisoMedicoMixin, PermisoAltoMixin
from acceso.mixins import permiso_medico_required
from acceso.access import HospitalAccessMixin, visibles_para
from acceso.access import filtrar_queryset


class PacienteListView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, ListView
):
    model = Paciente
    template_name = "paciente/lista_paciente.html"
    context_object_name = "pacientes"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("hospital").order_by("-id")

        # Filtros de búsqueda
        q = (self.request.GET.get("q") or "").strip()
        hospital_id = (self.request.GET.get("hospital") or "").strip()

        qs = visibles_para(Paciente, self.request.user)

        if q:
            qs = qs.filter(
                Q(nombre__icontains=q)
                | Q(apellido__icontains=q)
                | Q(telefono__icontains=q)
            )
        if hospital_id:
            qs = qs.filter(hospital_id=hospital_id)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        es_alto = (
            user.is_superuser
            or user.usuariorol_set.filter(
                rol__nombre__in=["DIRECCIÓN", "SISTEMAS"]
            ).exists()
        )
        context["es_director"] = es_alto

        hospital_usuario = user.usuariohospital_set.first()
        if hospital_usuario:
            context["hospital_nombre"] = hospital_usuario.hospital.nombre

        return context


class PacienteCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "paciente/crear_paciente.html"
    success_url = reverse_lazy("paciente:lista_paciente")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        paciente = form.save(commit=False)
        # El hospital ya se filtra/oculta en el formulario con filtrar_queryset
        paciente.save()
        return redirect(self.success_url)


class PacienteUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "paciente/crear_paciente.html"
    success_url = reverse_lazy("paciente:lista_paciente")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        paciente = form.save(commit=False)
        # El hospital ya se filtra/oculta en el formulario con filtrar_queryset
        paciente.save()
        return redirect(self.success_url)


class PacienteDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Paciente
    template_name = "paciente/confirmar_eliminar.html"
    success_url = reverse_lazy("paciente:lista_paciente")


@permiso_medico_required
def detalle_paciente(request, paciente_id):
    paciente = get_object_or_404(visibles_para(Paciente, request.user), id=paciente_id)

    asignacion_activa = (
        AsignacionCama.objects.filter(paciente=paciente, fecha_salida__isnull=True)
        .select_related("cama", "cama__habitacion", "cama__habitacion__area")
        .first()
    )

    historial = AsignacionCama.objects.filter(paciente=paciente).select_related(
        "cama", "cama__habitacion", "cama__habitacion__area"
    )

    return render(
        request,
        "paciente/detalle_paciente.html",
        {
            "paciente": paciente,
            "asignacion_activa": asignacion_activa,
            "historial": historial,
        },
    )
