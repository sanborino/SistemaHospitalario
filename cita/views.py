from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Cita
from .forms import CitaForm
    
class CitaListView(ListView):
    model = Cita
    template_name = "cita/lista.html"
    context_object_name = "citas"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("hospital", "paciente", "medico")
            .order_by("-fecha", "-hora", "-id")
        )

        paciente_id = (self.request.GET.get("paciente") or "").strip()
        medico_id = (self.request.GET.get("medico") or "").strip()
        estado = (self.request.GET.get("estado") or "").strip()
        fecha = (self.request.GET.get("fecha") or "").strip()
        hospital_id = (self.request.GET.get("hospital") or "").strip()

        # Si NO hay ningún filtro, devolver queryset vacío
        if not any([paciente_id, medico_id, estado, fecha, hospital_id]):
            return qs.none()

        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)
        if medico_id:
            qs = qs.filter(medico_id=medico_id)
        if estado:
            qs = qs.filter(estado=estado)
        if fecha:
            qs = qs.filter(fecha=fecha)
        if hospital_id:
            qs = qs.filter(hospital_id=hospital_id)

        return qs




class CitaDetailView(DetailView):
    model = Cita
    template_name = "cita/detalle.html"
    context_object_name = "cita"


class CitaCreateView(CreateView):
    model = Cita
    form_class = CitaForm
    template_name = "cita/formulario.html"

    def get_initial(self):
        initial = super().get_initial()
        # Precargar desde querystring si vienes desde paciente o médico:
        paciente_id = self.request.GET.get("paciente")
        medico_id = self.request.GET.get("medico")
        hospital_id = self.request.GET.get("hospital")

        if paciente_id:
            initial["paciente"] = paciente_id
        if medico_id:
            initial["medico"] = medico_id
        if hospital_id:
            initial["hospital"] = hospital_id

        return initial

    def get_success_url(self):
        return reverse_lazy("cita:detalle_cita", kwargs={"pk": self.object.pk})


class CitaUpdateView(UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = "cita/formulario.html"

    def get_success_url(self):
        return reverse_lazy("cita:detalle_cita", kwargs={"pk": self.object.pk})


class CitaDeleteView(DeleteView):
    model = Cita
    template_name = "cita/confirmar_eliminar.html"
    success_url = reverse_lazy("cita:lista_cita")


class CitaCalendarioView(TemplateView):
    template_name = "cita/calendario.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()

        # Mostrar próximas citas (hoy en adelante), ordenadas
        proximas = (
            Cita.objects
            .select_related("hospital", "paciente", "medico")
            .filter(fecha__gte=hoy)
            .order_by("fecha", "hora")
        )

        ctx["hoy"] = hoy
        ctx["proximas"] = proximas[:50]  # límite simple para no cargar demasiado
        return ctx