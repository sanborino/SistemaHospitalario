from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from .models import Cita
from .forms import CitaForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from acceso.models import UsuarioRol, UsuarioHospital
from acceso.mixins import PermisoMedicoMixin, PermisoAltoMixin


from acceso.access import HospitalAccessMixin, visibles_para


class CitaListView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, ListView
):
    model = Cita
    template_name = "cita/lista.html"
    context_object_name = "citas"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            visibles_para(Cita, self.request.user)
            .select_related("hospital", "paciente", "medico")
            .order_by("-fecha", "-hora", "-id")
        )

        paciente_id = self.request.GET.get("paciente")
        medico_id = self.request.GET.get("medico")
        estado = self.request.GET.get("estado")
        fecha = self.request.GET.get("fecha")
        hospital_id = self.request.GET.get("hospital")

        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)
        if medico_id:
            qs = qs.filter(medico_id=medico_id)
        if estado:
            qs = qs.filter(estado=estado)
        if fecha:
            qs = qs.filter(fecha=fecha)
        if hospital_id and self.request.user.has_perm("acceso.es_director"):
            qs = qs.filter(hospital_id=hospital_id)

        return qs


class CitaDetailView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, DetailView
):
    model = Cita
    template_name = "cita/detalle.html"
    context_object_name = "cita"


class CitaCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = Cita
    form_class = CitaForm
    template_name = "cita/formulario.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        cita = form.save(commit=False)
        # hospital ya filtrado en el form con filtrar_queryset
        cita.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cita:detalle_cita", kwargs={"pk": self.object.pk})


class CitaUpdateView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, UpdateView
):
    model = Cita
    form_class = CitaForm
    template_name = "cita/formulario.html"

    def get_success_url(self):
        return reverse_lazy("cita:detalle_cita", kwargs={"pk": self.object.pk})


class CitaDeleteView(
    LoginRequiredMixin, PermisoAltoMixin, HospitalAccessMixin, DeleteView
):
    model = Cita
    template_name = "cita/confirmar_eliminar.html"
    success_url = reverse_lazy("cita:lista_cita")


class CitaCalendarioView(LoginRequiredMixin, PermisoMedicoMixin, TemplateView):
    template_name = "cita/calendario.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        qs = (
            visibles_para(Cita, self.request.user)
            .select_related("hospital", "paciente", "medico")
            .filter(fecha__gte=hoy)
        )
        ctx["hoy"] = hoy
        ctx["proximas"] = qs.order_by("fecha", "hora")[:50]
        return ctx
