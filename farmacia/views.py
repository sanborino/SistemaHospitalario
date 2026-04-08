from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import (
    Medicamento,
    Receta,
    RecetaDetalle,
    Dispensacion,
    DispensacionDetalle,
)
from .forms import MedicamentoForm, RecetaForm, RecetaDetalleForm, DispensacionForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from farmacia.models import Medicamento
from facturacion.models import Cargo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from paciente.models import Paciente
from personal.models import Medico
from acceso.mixins import permiso_farmacia_required
from acceso.mixins import PermisoFarmaciaMixin, PermisoAltoMixin, PermisoMedicoMixin


# -----------------------
# Medicamentos
# -----------------------


class MedicamentoListView(LoginRequiredMixin, PermisoFarmaciaMixin, ListView):
    model = Medicamento
    template_name = "farmacia/medicamento_list.html"
    context_object_name = "medicamentos"
    paginate_by = 15
    ordering = ["nombre"]

    def get_queryset(self):
        queryset = Medicamento.objects.all()

        # --- Filtros ---
        nombre = self.request.GET.get("nombre")
        categoria = self.request.GET.get("categoria")
        presentacion = self.request.GET.get("presentacion")
        stock_min = self.request.GET.get("stock_min")

        if nombre:
            queryset = queryset.filter(nombre__icontains=nombre)

        if categoria:
            queryset = queryset.filter(categoria_id=categoria)

        if presentacion:
            queryset = queryset.filter(presentacion__icontains=presentacion)

        if stock_min:
            queryset = queryset.filter(stock__lte=stock_min)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Para selects dinámicos
        context["categorias"] = Medicamento.objects.all().order_by("nombre")

        # Mantener valores seleccionados
        context["filtro_nombre"] = self.request.GET.get("nombre", "")
        context["filtro_categoria"] = self.request.GET.get("categoria", "")
        context["filtro_presentacion"] = self.request.GET.get("presentacion", "")
        context["filtro_stock_min"] = self.request.GET.get("stock_min", "")

        return context


class MedicamentoCreateView(LoginRequiredMixin, PermisoFarmaciaMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = "farmacia/medicamento_form.html"
    success_url = reverse_lazy("farmacia:medicamento_list")


class MedicamentoUpdateView(LoginRequiredMixin, PermisoFarmaciaMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = "farmacia/medicamento_form.html"
    success_url = reverse_lazy("farmacia:medicamento_list")


class MedicamentoDetailView(LoginRequiredMixin, PermisoFarmaciaMixin, DetailView):
    model = Medicamento
    template_name = "farmacia/medicamento_detalle.html"
    context_object_name = "medicamento"


class MedicamentoDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Medicamento
    template_name = "farmacia/medicamento_confirm_delete.html"
    success_url = reverse_lazy("medicamento_list")


# -----------------------
# Recetas
# -----------------------


class RecetaListView(LoginRequiredMixin, PermisoMedicoMixin, ListView):
    model = Receta
    template_name = "farmacia/receta_list.html"
    context_object_name = "recetas"
    paginate_by = 10
    ordering = ["-fecha"]

    def get_queryset(self):
        queryset = Receta.objects.filter(dispensacion__isnull=True)

        # --- Filtros ---
        paciente_id = self.request.GET.get("paciente")
        medico_id = self.request.GET.get("medico")
        numero = self.request.GET.get("numero")
        fecha_desde = self.request.GET.get("desde")
        fecha_hasta = self.request.GET.get("hasta")

        if paciente_id:
            queryset = queryset.filter(paciente_id=paciente_id)

        if medico_id:
            queryset = queryset.filter(medico_id=medico_id)

        if numero:
            queryset = queryset.filter(id=numero)

        if fecha_desde:
            queryset = queryset.filter(fecha__date__gte=fecha_desde)

        if fecha_hasta:
            queryset = queryset.filter(fecha__date__lte=fecha_hasta)

        return queryset.select_related("paciente", "medico")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["pacientes"] = Paciente.objects.all().order_by("apellido", "nombre")
        context["medicos"] = Medico.objects.all().order_by("apellido", "nombre")

        # Mantener valores seleccionados
        context["filtro_paciente"] = self.request.GET.get("paciente", "")
        context["filtro_medico"] = self.request.GET.get("medico", "")
        context["filtro_numero"] = self.request.GET.get("numero", "")
        context["filtro_desde"] = self.request.GET.get("desde", "")
        context["filtro_hasta"] = self.request.GET.get("hasta", "")

        return context


class RecetaCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = "farmacia/receta_form.html"

    def get_success_url(self):
        # Redirige al formulario para agregar medicamentos
        return reverse_lazy(
            "farmacia:receta_detalle_add", kwargs={"receta_id": self.object.pk}
        )


class RecetaDetailView(LoginRequiredMixin, PermisoMedicoMixin, DetailView):
    model = Receta
    template_name = "farmacia/receta_detalle.html"
    context_object_name = "receta"

    def get_queryset(self):
        # Solo recetas que NO han sido surtidas
        return Receta.objects.filter(dispensacion__isnull=True)


class RecetaDetalleCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = RecetaDetalle
    form_class = RecetaDetalleForm
    template_name = "farmacia/receta_detalle_form.html"

    def form_valid(self, form):
        receta_id = self.kwargs["receta_id"]
        form.instance.receta_id = receta_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "farmacia:receta_detalle", kwargs={"pk": self.kwargs["receta_id"]}
        )


class RecetaDetalleUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = RecetaDetalle
    form_class = RecetaDetalleForm
    template_name = "farmacia/receta_detalle_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "farmacia:receta_detalle", kwargs={"pk": self.object.receta_id}
        )


class RecetaDetalleDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = RecetaDetalle
    template_name = "farmacia/receta_detalle_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "farmacia:receta_detalle", kwargs={"pk": self.object.receta_id}
        )


# -----------------------
# Dispensaciones
# -----------------------


class DispensacionListView(LoginRequiredMixin, PermisoFarmaciaMixin, ListView):
    model = Receta
    template_name = "farmacia/dispensacion_list.html"
    context_object_name = "recetas"

    def get_queryset(self):
        # Solo recetas que NO han sido surtidas
        return Receta.objects.filter(dispensacion__isnull=True)


class DispensacionCreateView(LoginRequiredMixin, PermisoFarmaciaMixin, CreateView):
    model = Dispensacion
    form_class = DispensacionForm
    template_name = "farmacia/dispensacion_form.html"
    success_url = reverse_lazy("farmacia:dispensacion_list")


@permiso_farmacia_required
def dispensacion_create(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)

    if Dispensacion.objects.filter(receta=receta).exists():
        dispensacion = Dispensacion.objects.get(receta=receta)
        messages.error(
            request, "Esta receta ya fue surtida y no puede volver a dispensarse."
        )
        return redirect("farmacia:dispensacion_detalle", pk=dispensacion.pk)

    detalles = receta.recetadetalle_set.all()  # RecetaDetalle

    if request.method == "POST":
        form = DispensacionForm(request.POST)

        if form.is_valid():
            # Validar primero cantidades y stock ANTES de guardar
            for d in detalles:
                cantidad_entregar = int(request.POST.get(f"entregar_{d.id}", 0))

                if cantidad_entregar > 0:
                    if cantidad_entregar > d.cantidad:
                        messages.error(
                            request,
                            f"No puedes dispensar más de lo recetado para {d.medicamento.nombre}. "
                            f"Recetado: {d.cantidad}",
                        )
                        return redirect(request.path)

                    if cantidad_entregar > d.medicamento.stock:
                        messages.error(
                            request,
                            f"No hay suficiente stock de {d.medicamento.nombre}. "
                            f"Disponible: {d.medicamento.stock}",
                        )
                        return redirect(request.path)

            # Si todas las validaciones pasan, ahora sí guardamos la dispensación
            dispensacion = form.save(commit=False)
            dispensacion.receta = receta
            dispensacion.save()

            # Crear detalles de dispensación y descontar inventario
            for d in detalles:
                cantidad_entregar = int(request.POST.get(f"entregar_{d.id}", 0))
                if cantidad_entregar > 0:
                    DispensacionDetalle.objects.create(
                        dispensacion=dispensacion,
                        medicamento=d.medicamento,
                        cantidad=cantidad_entregar,
                    )
                    d.medicamento.stock -= cantidad_entregar
                    d.medicamento.save()

            messages.success(request, "Dispensación realizada correctamente.")
            return redirect("farmacia:dispensacion_detalle", pk=dispensacion.pk)

    else:
        form = DispensacionForm()

    return render(
        request,
        "farmacia/dispensacion_form.html",
        {
            "form": form,
            "receta": receta,
            "detalles": detalles,
        },
    )


class DispensacionDetailView(LoginRequiredMixin, PermisoFarmaciaMixin, DetailView):
    model = Dispensacion
    template_name = "farmacia/dispensacion_detail.html"
    context_object_name = "dispensacion"


@permiso_farmacia_required
def dispensar_medicamentos(request, id):
    dispensacion = get_object_or_404(Dispensacion, pk=id)

    for detalle in dispensacion.detalles.all():
        Cargo.objects.create(
            paciente=dispensacion.receta.paciente,
            descripcion=f"Medicamento: {detalle.medicamento.nombre}",
            cantidad=detalle.cantidad,
            precio_unitario=detalle.medicamento.precio,
            dispensacion=dispensacion,
        )

    messages.success(request, "Medicamentos dispensados y cargos generados.")
    return redirect("farmacia:dispensacion_detail", id)
