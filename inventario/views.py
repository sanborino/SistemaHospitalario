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


class InsumoListView(LoginRequiredMixin, ListView):
    model = Insumo
    template_name = "inventario/insumo_lista.html"
    context_object_name = "insumos"
    paginate_by = 10
    ordering = ["nombre"]


class InsumoDetailView(LoginRequiredMixin, DetailView):
    model = Insumo
    template_name = "inventario/insumo_detalle.html"
    context_object_name = "insumo"


class InsumoCreateView(LoginRequiredMixin, CreateView):
    model = Insumo
    form_class = InsumoForm
    template_name = "inventario/insumo_formulario.html"

    def get_success_url(self):
        return reverse_lazy("inventario:detalle_insumo", kwargs={"pk": self.object.pk})


class InsumoUpdateView(LoginRequiredMixin, UpdateView):
    model = Insumo
    form_class = InsumoForm
    template_name = "inventario/insumo_formulario.html"

    def get_success_url(self):
        return reverse_lazy("inventario:detalle_insumo", kwargs={"pk": self.object.pk})


class InsumoDeleteView(LoginRequiredMixin, DeleteView):
    model = Insumo
    template_name = "inventario/insumo_confirmar_eliminar.html"
    context_object_name = "insumo"
    success_url = reverse_lazy("inventario:lista_insumo")


class MovimientoListView(LoginRequiredMixin, ListView):
    model = MovimientoInventario
    template_name = "inventario/movimiento_lista.html"
    context_object_name = "movimientos"
    paginate_by = 10
    ordering = ["-fecha"]

    def get_queryset(self):
        return super().get_queryset().select_related("insumo", "realizado_por")


class MovimientoDetailView(LoginRequiredMixin, DetailView):
    model = MovimientoInventario
    template_name = "inventario/movimiento_detalle.html"
    context_object_name = "movimiento"


class MovimientoCreateView(LoginRequiredMixin, CreateView):
    model = MovimientoInventario
    form_class = MovimientoInventarioForm
    template_name = "inventario/movimiento_formulario.html"

    def get_success_url(self):
        return reverse_lazy(
            "inventario:detalle_movimiento", kwargs={"pk": self.object.pk}
        )


class MovimientoUpdateView(LoginRequiredMixin, UpdateView):
    model = MovimientoInventario
    form_class = MovimientoInventarioForm
    template_name = "inventario/movimiento_formulario.html"

    def get_success_url(self):
        return reverse_lazy(
            "inventario:detalle_movimiento", kwargs={"pk": self.object.pk}
        )


class MovimientoDeleteView(LoginRequiredMixin, DeleteView):
    model = MovimientoInventario
    template_name = "inventario/movimiento_confirmar_eliminar.html"
    context_object_name = "movimiento"
    success_url = reverse_lazy("inventario:lista_movimiento")

