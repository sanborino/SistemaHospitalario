from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Turno, TurnoPersonal, Asistencia
from .forms import TurnoForm, TurnoPersonalForm, AsistenciaForm
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.utils import timezone
from acceso.models import UsuarioRol
import csv
from django.http import HttpResponse
from .forms import AsistenciaForm


# -----------------------
# TURNOS
# -----------------------


class TurnoListView(LoginRequiredMixin, ListView):
    model = Turno
    template_name = "turnos/turno_list.html"


class TurnoCreateView(LoginRequiredMixin, CreateView):
    model = Turno
    form_class = TurnoForm
    template_name = "turnos/turno_form.html"
    success_url = reverse_lazy("turno:turno_list")


class TurnoUpdateView(LoginRequiredMixin, UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name = "turnos/turno_form.html"
    success_url = reverse_lazy("turno:turno_list")


class TurnoDeleteView(LoginRequiredMixin, DeleteView):
    model = Turno
    template_name = "turnos/turno_confirm_delete.html"
    success_url = reverse_lazy("turno:turno_list")


# -----------------------
# TURNO PERSONAL
# -----------------------


class TurnoPersonalListView(LoginRequiredMixin, ListView):
    model = TurnoPersonal
    template_name = "turnos/turnopersonal_list.html"


class TurnoPersonalCreateView(LoginRequiredMixin, CreateView):
    model = TurnoPersonal
    form_class = TurnoPersonalForm
    template_name = "turnos/turnopersonal_form.html"
    success_url = reverse_lazy("turno:turnopersonal_list")


class TurnoPersonalUpdateView(LoginRequiredMixin, UpdateView):
    model = TurnoPersonal
    form_class = TurnoPersonalForm
    template_name = "turnos/turnopersonal_form.html"
    success_url = reverse_lazy("turno:turnopersonal_list")


class TurnoPersonalDeleteView(LoginRequiredMixin, DeleteView):
    model = TurnoPersonal
    template_name = "turnos/turnopersonal_confirm_delete.html"
    success_url = reverse_lazy("turno:turnopersonal_list")


# -----------------------
# ASISTENCIA
# -----------------------


# Función para validar si el usuario es Director


class AsistenciaListView(LoginRequiredMixin, ListView):
    model = Asistencia
    template_name = "turnos/asistencia_list.html"
    context_object_name = "asistencias"

    def get_queryset(self):
        hoy = timezone.localdate()
        user = self.request.user

        # Si es director, ve todas las asistencias del día
        if UsuarioRol.objects.filter(usuario=user, rol__nombre="DIRECCION").exists():
            return Asistencia.objects.filter(fecha=hoy).order_by("-hora_entrada")

        # Si no, solo ve sus propias asistencias
        return Asistencia.objects.filter(usuario=user, fecha=hoy).order_by(
            "-hora_entrada"
        )


class AsistenciaCreateView(LoginRequiredMixin, CreateView):
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


class AsistenciaUpdateView(LoginRequiredMixin, UpdateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = "turnos/asistencia_form.html"
    success_url = reverse_lazy("turno:asistencia_list")


class AsistenciaDeleteView(LoginRequiredMixin, DeleteView):
    model = Asistencia
    template_name = "turnos/asistencia_confirm_delete.html"
    success_url = reverse_lazy("turno:asistencia_list")


def es_director(user):
    return (
        user.is_authenticated
        and UsuarioRol.objects.filter(usuario=user, rol__nombre="DIRECCIÓN").exists()
    )


@user_passes_test(es_director)
def reporte_asistencias(request):
    asistencias = Asistencia.objects.all().order_by("-fecha", "-hora_entrada")
    return render(
        request, "turnos/reporte_asistencias.html", {"asistencias": asistencias}
    )


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
