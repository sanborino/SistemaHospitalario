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
from django.contrib.auth.decorators import login_required



class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = "paciente/lista_paciente.html"
    context_object_name = "pacientes"
    paginate_by = 10

    def get_queryset(self):
        q = (self.request.GET.get("q") or "").strip()
        hospital_id = (self.request.GET.get("hospital") or "").strip()

        # ✅ Si no hay filtros, no mostramos nada
        if not q and not hospital_id:
            return Paciente.objects.none()

        qs = super().get_queryset().select_related("hospital").order_by("-id")

        if q:
            qs = qs.filter(
                Q(nombre__icontains=q)
                | Q(apellido__icontains=q)
                | Q(telefono__icontains=q)
            )

        if hospital_id:
            qs = qs.filter(hospital_id=hospital_id)

        return qs


class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "paciente/crear_paciente.html"

    def get_success_url(self):
        return reverse_lazy(
            "paciente:detalle_paciente", kwargs={"paciente_id": self.object.pk}
        )


class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "paciente/crear_paciente.html"

    def get_success_url(self):
        return reverse_lazy(
            "paciente:detalle_paciente", kwargs={"paciente_id": self.object.pk}
        )


class PacienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Paciente
    template_name = "paciente/confirmar_eliminar.html"
    success_url = reverse_lazy("paciente:lista_paciente")

@login_required
def detalle_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

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
