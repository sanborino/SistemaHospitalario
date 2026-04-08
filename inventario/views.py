from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Insumo, MovimientoInventario
from .forms import InsumoForm, MovimientoInventarioForm
from acceso.mixins import PermisoAltoMixin, PermisoMedicoMixin


class InsumoListView(LoginRequiredMixin, PermisoAltoMixin, ListView):
    model = Insumo
    template_name = "inventario/insumo_lista.html"
    context_object_name = "insumos"
    paginate_by = 10
    ordering = ["nombre"]

    def get_queryset(self):
        queryset = super().get_queryset()
        nombre = self.request.GET.get("nombre", None)
        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)
        return queryset


class InsumoDetailView(LoginRequiredMixin, PermisoAltoMixin, DetailView):
    model = Insumo
    template_name = "inventario/insumo_detalle.html"
    context_object_name = "insumo"


class InsumoCreateView(LoginRequiredMixin, PermisoAltoMixin, CreateView):
    model = Insumo
    form_class = InsumoForm
    template_name = "inventario/insumo_formulario.html"

    def get_success_url(self):
        return reverse_lazy("inventario:detalle_insumo", kwargs={"pk": self.object.pk})


class InsumoUpdateView(LoginRequiredMixin, PermisoAltoMixin, UpdateView):
    model = Insumo
    form_class = InsumoForm
    template_name = "inventario/insumo_formulario.html"

    def get_success_url(self):
        return reverse_lazy("inventario:detalle_insumo", kwargs={"pk": self.object.pk})


class InsumoDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Insumo
    template_name = "inventario/insumo_confirmar_eliminar.html"
    context_object_name = "insumo"
    success_url = reverse_lazy("inventario:lista_insumo")


class MovimientoListView(LoginRequiredMixin, PermisoMedicoMixin, ListView):
    model = MovimientoInventario
    template_name = "inventario/movimiento_lista.html"
    context_object_name = "movimientos"
    paginate_by = 10
    ordering = ["-fecha"]

    def get_queryset(self):
        queryset = super().get_queryset().select_related("insumo", "realizado_por")
        nombre = self.request.GET.get("nombre", None)
        if nombre:
            queryset = queryset.filter(insumo__nombre__icontains=nombre)
        return queryset


class MovimientoDetailView(LoginRequiredMixin, PermisoMedicoMixin, DetailView):
    model = MovimientoInventario
    template_name = "inventario/movimiento_detalle.html"
    context_object_name = "movimiento"


class MovimientoCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = MovimientoInventario
    form_class = MovimientoInventarioForm
    template_name = "inventario/movimiento_formulario.html"

    def form_valid(self, form):
        form.instance.realizado_por = self.request.user  # 👈 asigna usuario logueado
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "inventario:detalle_movimiento", kwargs={"pk": self.object.pk}
        )


class MovimientoUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = MovimientoInventario
    form_class = MovimientoInventarioForm
    template_name = "inventario/movimiento_formulario.html"

    def form_valid(self, form):
        # Mantener el usuario original o reasignar al logueado, según tu lógica
        if not form.instance.realizado_por:
            form.instance.realizado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "inventario:detalle_movimiento", kwargs={"pk": self.object.pk}
        )


class MovimientoDeleteView(LoginRequiredMixin, PermisoMedicoMixin, DeleteView):
    model = MovimientoInventario
    template_name = "inventario/movimiento_confirmar_eliminar.html"
    context_object_name = "movimiento"
    success_url = reverse_lazy("inventario:lista_movimiento")
