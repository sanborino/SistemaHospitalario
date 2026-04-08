from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Area, Habitacion, Cama
from .forms import AreaForm, HabitacionForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Habitacion, Cama, Area
from acceso.mixins import PermisoAltoMixin
from acceso.mixins import permiso_alto_required, permiso_medico_required


class AreaListView(LoginRequiredMixin, PermisoAltoMixin, ListView):
    model = Area
    template_name = "infraestructura/area_lista.html"
    context_object_name = "areas"
    paginate_by = 10
    ordering = ["hospital__nombre", "nombre"]


class AreaDetailView(LoginRequiredMixin, PermisoAltoMixin, DetailView):
    model = Area
    template_name = "infraestructura/area_detalle.html"
    context_object_name = "area"


class AreaCreateView(LoginRequiredMixin, PermisoAltoMixin, CreateView):
    model = Area
    form_class = AreaForm
    template_name = "infraestructura/area_formulario.html"

    def get_success_url(self):
        return reverse_lazy(
            "infraestructura:detalle_area", kwargs={"pk": self.object.pk}
        )


class AreaUpdateView(LoginRequiredMixin, PermisoAltoMixin, UpdateView):
    model = Area
    form_class = AreaForm
    template_name = "infraestructura/area_formulario.html"

    def get_success_url(self):
        return reverse_lazy(
            "infraestructura:detalle_area", kwargs={"pk": self.object.pk}
        )


class AreaDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Area
    template_name = "infraestructura/area_confirmar_eliminar.html"
    success_url = reverse_lazy("infraestructura:lista_area")


class HabitacionListView(LoginRequiredMixin, PermisoAltoMixin, ListView):
    model = Habitacion
    template_name = "infraestructura/habitacion_lista.html"
    context_object_name = "habitaciones"
    paginate_by = 10
    ordering = ["hospital__nombre", "area__nombre", "numero"]


class HabitacionDetailView(LoginRequiredMixin, PermisoAltoMixin, DetailView):
    model = Habitacion
    template_name = "infraestructura/habitacion_detalle.html"
    context_object_name = "habitacion"


class HabitacionCreateView(LoginRequiredMixin, PermisoAltoMixin, CreateView):
    model = Habitacion
    form_class = HabitacionForm
    template_name = "infraestructura/habitacion_formulario.html"

    def get_success_url(self):
        return reverse_lazy(
            "infraestructura:detalle_habitacion", kwargs={"pk": self.object.pk}
        )


class HabitacionUpdateView(LoginRequiredMixin, PermisoAltoMixin, UpdateView):
    model = Habitacion
    form_class = HabitacionForm
    template_name = "infraestructura/habitacion_formulario.html"

    def get_success_url(self):
        return reverse_lazy(
            "infraestructura:detalle_habitacion", kwargs={"pk": self.object.pk}
        )


class HabitacionDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Habitacion
    template_name = "infraestructura/habitacion_confirmar_eliminar.html"
    success_url = reverse_lazy("infraestructura:lista_habitacion")


# Vista antigua residual si se usa como dashboard
@permiso_alto_required
def infraestructura_dashboard(request):
    return render(request, "infraestructura/dashboard.html")


@permiso_alto_required
def lista_habitaciones(request):
    habitaciones = Habitacion.objects.select_related("area", "hospital")
    return render(
        request,
        "infraestructura/lista_habitaciones.html",
        {"habitaciones": habitaciones},
    )


@permiso_alto_required
def lista_camas(request):
    camas = Cama.objects.select_related("habitacion", "habitacion__area")
    return render(request, "infraestructura/lista_camas.html", {"camas": camas})


@permiso_alto_required
def crear_cama(request):
    habitaciones = Habitacion.objects.all()

    if request.method == "POST":
        habitacion_id = request.POST.get("habitacion")
        numero = request.POST.get("numero")
        tipo = request.POST.get("tipo")

        habitacion = get_object_or_404(Habitacion, id=habitacion_id)

        Cama.objects.create(
            habitacion=habitacion, numero=numero, tipo=tipo, estado="DISPONIBLE"
        )

        return redirect("infraestructura:infra_lista_camas")

    return render(
        request,
        "infraestructura/crear_cama.html",
        {
            "habitaciones": habitaciones,
        },
    )


@permiso_alto_required
def editar_cama(request, cama_id):
    cama = get_object_or_404(Cama, id=cama_id)
    habitaciones = Habitacion.objects.all()

    if request.method == "POST":
        cama.numero = request.POST.get("numero")
        cama.tipo = request.POST.get("tipo")
        cama.estado = request.POST.get("estado")
        habitacion_id = request.POST.get("habitacion")
        cama.habitacion = get_object_or_404(Habitacion, id=habitacion_id)

        cama.save()
        return redirect("infraestructura:infra_lista_camas")

    return render(
        request,
        "infraestructura/editar_cama.html",
        {
            "cama": cama,
            "habitaciones": habitaciones,
        },
    )


@permiso_alto_required
def eliminar_cama(request, cama_id):
    cama = get_object_or_404(Cama, id=cama_id)

    if request.method == "POST":
        cama.delete()
        return redirect("infraestructura:infra_lista_camas")

    return render(request, "infraestructura/eliminar_cama.html", {"cama": cama})
