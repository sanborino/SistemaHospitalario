from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Turno, TurnoPersonal, Asistencia
from .forms import TurnoForm, TurnoPersonalForm, AsistenciaForm
from django.utils import timezone

# -----------------------
# TURNOS
# -----------------------

class TurnoListView(ListView):
    model = Turno
    template_name = "turnos/turno_list.html"


class TurnoCreateView(CreateView):
    model = Turno
    form_class = TurnoForm
    template_name = "turnos/turno_form.html"
    success_url = reverse_lazy("turno:turno_list")


class TurnoUpdateView(UpdateView):
    model = Turno
    form_class = TurnoForm
    template_name = "turnos/turno_form.html"
    success_url = reverse_lazy("turno:turno_list")


class TurnoDeleteView(DeleteView):
    model = Turno
    template_name = "turnos/turno_confirm_delete.html"
    success_url = reverse_lazy("turno:turno_list")


# -----------------------
# TURNO PERSONAL
# -----------------------

class TurnoPersonalListView(ListView):
    model = TurnoPersonal
    template_name = "turnos/turnopersonal_list.html"


class TurnoPersonalCreateView(CreateView):
    model = TurnoPersonal
    form_class = TurnoPersonalForm
    template_name = "turnos/turnopersonal_form.html"
    success_url = reverse_lazy("turno:turnopersonal_list")


class TurnoPersonalUpdateView(UpdateView):
    model = TurnoPersonal
    form_class = TurnoPersonalForm
    template_name = "turnos/turnopersonal_form.html"
    success_url = reverse_lazy("turno:turnopersonal_list")


class TurnoPersonalDeleteView(DeleteView):
    model = TurnoPersonal
    template_name = "turnos/turnopersonal_confirm_delete.html"
    success_url = reverse_lazy("turno:turnopersonal_list")


# -----------------------
# ASISTENCIA
# -----------------------

class AsistenciaListView(ListView):
    model = Asistencia
    template_name = "turnos/asistencia_list.html"


class AsistenciaCreateView(CreateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = "turnos/asistencia_form.html"
    success_url = reverse_lazy("turno:asistencia_list")
    
    def form_valid(self, form):
        usuario = form.cleaned_data['usuario']
        hoy = timezone.localdate()

        # Buscar si ya existe asistencia de este usuario hoy
        asistencia = Asistencia.objects.filter(usuario=usuario, fecha=hoy).first()

        if asistencia:
            # Ya existe → registrar salida
            asistencia.hora_salida = timezone.localtime().time()
            asistencia.save()
        else:
            # No existe → registrar entrada
            nueva = form.save(commit=False)
            nueva.hora_entrada = timezone.localtime().time()
            nueva.save()

        return super().form_valid(form)


class AsistenciaUpdateView(UpdateView):
    model = Asistencia
    form_class = AsistenciaForm
    template_name = "turnos/asistencia_form.html"
    success_url = reverse_lazy("turno:asistencia_list")


class AsistenciaDeleteView(DeleteView):
    model = Asistencia
    template_name = "turnos/asistencia_confirm_delete.html"
    success_url = reverse_lazy("turno:asistencia_list")