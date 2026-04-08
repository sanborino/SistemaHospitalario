from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Hospital
from .forms import HospitalForm
from acceso.mixins import PermisoAltoMixin


class HospitalListView(LoginRequiredMixin, PermisoAltoMixin, ListView):
    model = Hospital
    template_name = "hospital/lista.html"
    context_object_name = "hospitales"
    paginate_by = 10
    ordering = ["nombre"]


class HospitalDetailView(LoginRequiredMixin, PermisoAltoMixin, DetailView):
    model = Hospital
    template_name = "hospital/detalle.html"
    context_object_name = "hospital"


class HospitalCreateView(LoginRequiredMixin, PermisoAltoMixin, CreateView):
    model = Hospital
    form_class = HospitalForm
    template_name = "hospital/formulario.html"

    def get_success_url(self):
        return reverse_lazy("hospital:detalle_hospital", kwargs={"pk": self.object.pk})


class HospitalUpdateView(LoginRequiredMixin, PermisoAltoMixin, UpdateView):
    model = Hospital
    form_class = HospitalForm
    template_name = "hospital/formulario.html"

    def get_success_url(self):
        return reverse_lazy("hospital:detalle_hospital", kwargs={"pk": self.object.pk})


class HospitalDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Hospital
    template_name = "hospital/confirmar_eliminar.html"
    success_url = reverse_lazy("hospital:lista_hospital")
