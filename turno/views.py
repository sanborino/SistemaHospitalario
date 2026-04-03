from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Turno, TurnoPersonal, Asistencia
from .forms import TurnoForm, TurnoPersonalForm, AsistenciaForm
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


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


class AsistenciaListView(LoginRequiredMixin, ListView):
    model = Asistencia
    template_name = "turnos/asistencia_list.html"

    def get_queryset(self):
        hoy = timezone.localdate()
        return Asistencia.objects.filter(fecha=hoy).order_by("-hora_entrada")


class AsistenciaCreateView(LoginRequiredMixin, CreateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = "turnos/asistencia_form.html"
    success_url = reverse_lazy("turno:asistencia_list")

    def form_valid(self, form):
        usuario = form.cleaned_data["usuario"]
        hoy = timezone.localdate()

        # Buscar si ya existe asistencia de este usuario hoy
        asistencia = Asistencia.objects.filter(usuario=usuario, fecha=hoy).first()

        if asistencia:
            # Ya existe → registrar salida
            asistencia.hora_salida = timezone.localtime().time()
            asistencia.save()
            self.object = asistencia  # <- importante: vincular el objeto actualizado
        else:
            # No existe → registrar entrada
            nueva = form.save(commit=False)
            nueva.hora_entrada = timezone.localtime().time()
            nueva.save()
            self.object = nueva  # <- vincular el objeto creado

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
