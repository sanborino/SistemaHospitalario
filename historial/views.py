from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import HistorialClinico
from .forms import HistorialClinicoForm

class HistorialListView(ListView):
    model = HistorialClinico
    template_name = "historial/lista.html"
    context_object_name = "historiales"
    paginate_by = 10

    
    def get_queryset(self):
        qs = super().get_queryset().select_related("hospital", "paciente", "medico").order_by("-fecha", "-id")

        paciente_id = self.request.GET.get("paciente")
        hospital_id = self.request.GET.get("hospital")

        # Si NO hay filtros, devolver queryset vacío
        if not paciente_id and not hospital_id:
            return qs.none()

        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)
        if hospital_id:
            qs = qs.filter(hospital_id=hospital_id)

        return qs


class HistorialDetailView(DetailView):
    model = HistorialClinico
    template_name = "historial/detalle.html"
    context_object_name = "historial"


class HistorialCreateView(CreateView):
    model = HistorialClinico
    form_class = HistorialClinicoForm
    template_name = "historial/formulario.html"

    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        if self.object.cita:
            self.object.cita.estado = "atendida"
            self.object.cita.save(update_fields=["estado"])

        return response

    def get_initial(self):
        initial = super().get_initial()
        cita_id = self.request.GET.get("cita")
        
        
        if cita_id:
            from cita.models import Cita
            c = Cita.objects.select_related("hospital", "paciente", "medico").get(pk=cita_id)
            initial["cita"] = c.id
            initial["hospital"] = c.hospital_id
            initial["paciente"] = c.paciente_id
            initial["medico"] = c.medico_id

        
        paciente_id = self.request.GET.get("paciente")
        hospital_id = self.request.GET.get("hospital")
        if paciente_id:
            initial["paciente"] = paciente_id
        if hospital_id:
            initial["hospital"] = hospital_id
        return initial

    def get_success_url(self):
        return reverse_lazy("historial:detalle_historial", kwargs={"pk": self.object.pk})    


class HistorialUpdateView(UpdateView):
    model = HistorialClinico
    form_class = HistorialClinicoForm
    template_name = "historial/formulario.html"

    def get_success_url(self):
        return reverse_lazy("historial:detalle:_historial", kwargs={"pk": self.object.pk})


class HistorialDeleteView(DeleteView):
    model = HistorialClinico
    template_name = "historial/confirmar_eliminar.html"
    success_url = reverse_lazy("historial:lista_historial")