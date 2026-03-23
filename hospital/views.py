from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from acceso.models import UsuarioRol

from .models import Hospital
from .forms import HospitalForm


class HospitalListView(LoginRequiredMixin, ListView):
    model = Hospital
    template_name = "hospital/lista.html"
    context_object_name = "hospitales"
    paginate_by = 10
    ordering = ["nombre"]


class HospitalDetailView(LoginRequiredMixin, DetailView):
    model = Hospital
    template_name = "hospital/detalle.html"
    context_object_name = "hospital"


class HospitalCreateView(LoginRequiredMixin, CreateView):
    model = Hospital
    form_class = HospitalForm
    template_name = "hospital/formulario.html"

    def get_success_url(self):
        return reverse_lazy("hospital:detalle_hospital", kwargs={"pk": self.object.pk})


class HospitalUpdateView(LoginRequiredMixin, UpdateView):
    model = Hospital
    form_class = HospitalForm
    template_name = "hospital/formulario.html"

    def get_success_url(self):
        return reverse_lazy("hospital:detalle_hospital", kwargs={"pk": self.object.pk})


class HospitalDeleteView(LoginRequiredMixin, DeleteView):
    model = Hospital
    template_name = "hospital/confirmar_eliminar.html"
    success_url = reverse_lazy("hospital:lista_hospital")
