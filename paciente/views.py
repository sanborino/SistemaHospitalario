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
from acceso.models import UsuarioRol, UsuarioHospital
from acceso.mixins import PermisoMedicoMixin, PermisoAltoMixin
from acceso.mixins import permiso_medico_required


class PacienteListView(LoginRequiredMixin, PermisoMedicoMixin, ListView):
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


class PacienteCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "paciente/crear_paciente.html"
    success_url = reverse_lazy("paciente:paciente_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        paciente = form.save(commit=False)
        user = self.request.user

        # Refuerzo de seguridad: si no es director, forzar hospital correcto
        if not UsuarioRol.objects.filter(
            usuario=user, rol__nombre="DIRECCIÓN"
        ).exists():
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if hospital_usuario:
                paciente.hospital = hospital_usuario.hospital

        paciente.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Pasar hospital al contexto para mostrarlo en la plantilla
        hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
        if hospital_usuario:
            context["hospital_nombre"] = hospital_usuario.hospital.nombre
        return context


class PacienteUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "paciente/crear_paciente.html"

    def get_success_url(self):
        return reverse_lazy(
            "paciente:detalle_paciente", kwargs={"paciente_id": self.object.pk}
        )


class PacienteDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Paciente
    template_name = "paciente/confirmar_eliminar.html"
    success_url = reverse_lazy("paciente:lista_paciente")


@permiso_medico_required
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
