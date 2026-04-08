from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Turno, TurnoPersonal, Asistencia
from .forms import TurnoForm, TurnoPersonalForm, AsistenciaForm
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.utils import timezone
from acceso.models import UsuarioRol
import csv
from django.http import HttpResponse
from .forms import AsistenciaForm
from acceso.mixins import PermisoAltoMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from acceso.mixins import PermisoMedicoMixin, PermisoBasicoMixin


# -----------------------
# TURNOS
# -----------------------


class TurnoListView(LoginRequiredMixin, PermisoMedicoMixin, ListView):
    model = Turno
    template_name = "turnos/turno_list.html"


class TurnoCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = Turno
    form_class = TurnoForm
    template_name = "turnos/turno_form.html"
    success_url = reverse_lazy("turno:turno_list")


class TurnoUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name = "turnos/turno_form.html"
    success_url = reverse_lazy("turno:turno_list")


class TurnoDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Turno
    template_name = "turnos/turno_confirm_delete.html"
    success_url = reverse_lazy("turno:turno_list")


# -----------------------
# TURNO PERSONAL
# -----------------------


class TurnoPersonalListView(LoginRequiredMixin, PermisoMedicoMixin, ListView):
    model = TurnoPersonal
    template_name = "turnos/turnopersonal_list.html"


class TurnoPersonalCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = TurnoPersonal
    form_class = TurnoPersonalForm
    template_name = "turnos/turnopersonal_form.html"
    success_url = reverse_lazy("turno:turnopersonal_list")


class TurnoPersonalUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = TurnoPersonal
    form_class = TurnoPersonalForm
    template_name = "turnos/turnopersonal_form.html"
    success_url = reverse_lazy("turno:turnopersonal_list")


class TurnoPersonalDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = TurnoPersonal
    template_name = "turnos/turnopersonal_confirm_delete.html"
    success_url = reverse_lazy("turno:turnopersonal_list")


# -----------------------
# ASISTENCIA
# -----------------------


# Función para validar si el usuario es Director


class AsistenciaListView(PermisoBasicoMixin, ListView):
    model = Asistencia
    template_name = "turnos/asistencia_list.html"
    context_object_name = "asistencias"
    paginate_by = 10  # número de registros por página

    def get_queryset(self):
        user = self.request.user
        qs = Asistencia.objects.all().order_by("-fecha", "-hora_entrada")

        # Restricción por rol
        if not UsuarioRol.objects.filter(
            usuario=user, rol__nombre="DIRECCION"
        ).exists():
            qs = qs.filter(usuario=user)

        # Filtro por fechas
        fecha_inicio = self.request.GET.get("fecha_inicio")
        fecha_fin = self.request.GET.get("fecha_fin")

        if fecha_inicio and fecha_fin:
            qs = qs.filter(fecha__range=[fecha_inicio, fecha_fin])
        elif fecha_inicio:
            qs = qs.filter(fecha__gte=fecha_inicio)
        elif fecha_fin:
            qs = qs.filter(fecha__lte=fecha_fin)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fecha_inicio"] = self.request.GET.get("fecha_inicio", "")
        context["fecha_fin"] = self.request.GET.get("fecha_fin", "")
        return context


class AsistenciaCreateView(PermisoBasicoMixin, CreateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = "turnos/asistencia_form.html"
    success_url = reverse_lazy("turno:asistencia_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # pasamos el usuario al form
        return kwargs

    def form_valid(self, form):
        usuario = self.request.user  # <- siempre el usuario logueado
        hoy = timezone.localdate()

        # Buscar si ya existe asistencia de este usuario hoy
        asistencia = Asistencia.objects.filter(usuario=usuario, fecha=hoy).first()

        if asistencia:
            # Ya existe → registrar salida
            asistencia.hora_salida = timezone.localtime().time()
            asistencia.save()
            self.object = asistencia
        else:
            # No existe → registrar entrada
            nueva = form.save(commit=False)
            nueva.usuario = usuario  # <- asignamos el usuario logueado
            nueva.hora_entrada = timezone.localtime().time()
            nueva.save()
            self.object = nueva

        return redirect(self.success_url)


class AsistenciaUpdateView(PermisoBasicoMixin, UpdateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = "turnos/asistencia_form.html"
    success_url = reverse_lazy("turno:asistencia_list")


class AsistenciaDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Asistencia
    template_name = "turnos/asistencia_confirm_delete.html"
    success_url = reverse_lazy("turno:asistencia_list")


def es_director(user):
    return (
        user.is_authenticated
        and UsuarioRol.objects.filter(usuario=user, rol__nombre="DIRECCIÓN").exists()
    )


@login_required
@user_passes_test(es_director)
def reporte_asistencias(request):
    asistencias = Asistencia.objects.all().order_by("-fecha", "-hora_entrada")
    return render(
        request, "turnos/reporte_asistencias.html", {"asistencias": asistencias}
    )


@login_required
@user_passes_test(es_director)
def reporte_asistencias_excel(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="reporte_asistencias.csv"'

    writer = csv.writer(response)
    writer.writerow(["Usuario", "Fecha", "Hora entrada", "Hora salida"])

    asistencias = Asistencia.objects.all().order_by("-fecha", "-hora_entrada")
    for asistencia in asistencias:
        writer.writerow(
            [
                asistencia.usuario.username,
                asistencia.fecha,
                asistencia.hora_entrada or "",
                asistencia.hora_salida or "",
            ]
        )

    return response


def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs["user"] = self.request.user
    return kwargs
