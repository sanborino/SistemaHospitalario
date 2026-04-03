from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Urgencia, AtencionUrgencia, AltaUrgencia
from .forms import UrgenciaForm, AtencionUrgenciaForm, AltaUrgenciaForm
from facturacion.models import Cargo
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# CRUD Urgencia
class UrgenciaListView(LoginRequiredMixin, ListView):
    model = Urgencia
    template_name = "urgencia/urgencia_lista.html"
    context_object_name = "urgencias"
    paginate_by = 10
    ordering = ["-fecha_ingreso"]


class UrgenciaDetailView(LoginRequiredMixin, DetailView):
    model = Urgencia
    template_name = "urgencia/urgencia_detalle.html"
    context_object_name = "urgencia"


class UrgenciaCreateView(LoginRequiredMixin, CreateView):
    model = Urgencia
    form_class = UrgenciaForm
    template_name = "urgencia/urgencia_formulario.html"

    def get_success_url(self):
        return reverse_lazy("urgencia:detalle_urgencia", kwargs={"pk": self.object.pk})


class UrgenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = Urgencia
    form_class = UrgenciaForm
    template_name = "urgencia/urgencia_formulario.html"

    def get_success_url(self):
        return reverse_lazy("urgencia:detalle_urgencia", kwargs={"pk": self.object.pk})


class UrgenciaDeleteView(LoginRequiredMixin, DeleteView):
    model = Urgencia
    template_name = "urgencia/urgencia_confirmar_eliminar.html"
    success_url = reverse_lazy("urgencia:lista_urgencia")


# CRUD AtencionUrgencia
class AtencionUrgenciaListView(LoginRequiredMixin, ListView):
    model = AtencionUrgencia
    template_name = "urgencia/atencion_lista.html"
    context_object_name = "atenciones"
    paginate_by = 10
    ordering = ["-fecha"]

    def get_queryset(self):
        return super().get_queryset().select_related("urgencia", "medico")


class AtencionUrgenciaDetailView(LoginRequiredMixin, DetailView):
    model = AtencionUrgencia
    template_name = "urgencia/atencion_detalle.html"
    context_object_name = "atencion"


class AtencionUrgenciaCreateView(LoginRequiredMixin, CreateView):
    model = AtencionUrgencia
    form_class = AtencionUrgenciaForm
    template_name = "urgencia/atencion_formulario.html"

    def get_success_url(self):
        return reverse_lazy("urgencia:detalle_atencion", kwargs={"pk": self.object.pk})


class AtencionUrgenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = AtencionUrgencia
    form_class = AtencionUrgenciaForm
    template_name = "urgencia/atencion_formulario.html"

    def get_success_url(self):
        return reverse_lazy("urgencia:detalle_atencion", kwargs={"pk": self.object.pk})


class AtencionUrgenciaDeleteView(LoginRequiredMixin, DeleteView):
    model = AtencionUrgencia
    template_name = "urgencia/atencion_confirmar_eliminar.html"
    context_object_name = "atencion"
    success_url = reverse_lazy("urgencia:lista_atencion")


# CRUD AltaUrgencia
class AltaUrgenciaListView(LoginRequiredMixin, ListView):
    model = AltaUrgencia
    template_name = "urgencia/alta_lista.html"
    context_object_name = "altas"
    paginate_by = 10
    ordering = ["-fecha"]

    def get_queryset(self):
        return super().get_queryset().select_related("urgencia")


class AltaUrgenciaDetailView(LoginRequiredMixin, DetailView):
    model = AltaUrgencia
    template_name = "urgencia/alta_detalle.html"
    context_object_name = "alta"


class AltaUrgenciaCreateView(LoginRequiredMixin, CreateView):
    model = AltaUrgencia
    form_class = AltaUrgenciaForm
    template_name = "urgencia/alta_formulario.html"

    def get_success_url(self):
        return reverse_lazy("urgencia:detalle_alta", kwargs={"pk": self.object.pk})


class AltaUrgenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = AltaUrgencia
    form_class = AltaUrgenciaForm
    template_name = "urgencia/alta_formulario.html"

    def get_success_url(self):
        return reverse_lazy("urgencia:detalle_alta", kwargs={"pk": self.object.pk})


class AltaUrgenciaDeleteView(LoginRequiredMixin, DeleteView):
    model = AltaUrgencia
    template_name = "urgencia/alta_confirmar_eliminar.html"
    context_object_name = "alta"
    success_url = reverse_lazy("urgencia:lista_alta")

@login_required
def cerrar_urgencia(request, id):
    urgencia = get_object_or_404(Urgencia, pk=id)

    Cargo.objects.create(
        paciente=urgencia.paciente,
        descripcion="Atención de urgencias",
        cantidad=1,
        precio_unitario=500,  # tu tarifa
        urgencia=urgencia,
    )

    urgencia.estado = "CERRADO"
    urgencia.save()

    messages.success(request, "Urgencia cerrada y cargo generado.")
    return redirect("urgencia:detalle", id)
