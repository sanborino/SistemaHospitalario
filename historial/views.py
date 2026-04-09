from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import HistorialClinico
from .forms import HistorialClinicoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from acceso.mixins import PermisoMedicoMixin, PermisoAltoMixin


from acceso.access import HospitalAccessMixin, visibles_para


class HistorialListView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, ListView
):
    model = HistorialClinico
    template_name = "historial/lista.html"
    context_object_name = "historiales"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            visibles_para(HistorialClinico, self.request.user)
            .select_related("hospital", "paciente", "medico")
            .order_by("-fecha", "-id")
        )

        paciente_id = self.request.GET.get("paciente")
        hospital_id = self.request.GET.get("hospital")

        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)
        if hospital_id and self.request.user.has_perm("acceso.es_director"):
            qs = qs.filter(hospital_id=hospital_id)

        return qs


class HistorialDetailView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, DetailView
):
    model = HistorialClinico
    template_name = "historial/detalle.html"
    context_object_name = "historial"


class HistorialCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = HistorialClinico
    form_class = HistorialClinicoForm
    template_name = "historial/formulario.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        historial = form.save(commit=False)
        historial.save()
        self.object = historial  # Asignar self.object para get_success_url

        if historial.cita:
            historial.cita.estado = "atendida"
            historial.cita.save(update_fields=["estado"])

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy(
            "historial:detalle_historial", kwargs={"pk": self.object.pk}
        )


class HistorialUpdateView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, UpdateView
):
    model = HistorialClinico
    form_class = HistorialClinicoForm
    template_name = "historial/formulario.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy(
            "historial:detalle_historial", kwargs={"pk": self.object.pk}
        )


class HistorialDeleteView(
    LoginRequiredMixin, PermisoAltoMixin, HospitalAccessMixin, DeleteView
):
    model = HistorialClinico
    template_name = "historial/confirmar_eliminar.html"
    success_url = reverse_lazy("historial:lista_historial")
