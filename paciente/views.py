from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Paciente
from .forms import PacienteForm
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin



class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = "paciente/lista_pacientes.html"
    context_object_name = "pacientes"
    paginate_by = 10

    def get_queryset(self):
        q = (self.request.GET.get("q") or "").strip()
        hospital_id = (self.request.GET.get("hospital") or "").strip()

        # ✅ Si no hay filtros, no mostramos nada
        if not q and not hospital_id:
            return Paciente.objects.none()

        qs = (
            super()
            .get_queryset()
            .select_related("hospital")
            .order_by("-id")
        )

        if q:
            qs = qs.filter(
                Q(nombre__icontains=q) |
                Q(apellido__icontains=q) |
                Q(telefono__icontains=q)
            )

        if hospital_id:
            qs = qs.filter(hospital_id=hospital_id)

        return qs



class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "paciente/crear_paciente.html"
    
    def get_success_url(self):
        return reverse_lazy("paciente:detalle_paciente", kwargs={"pk": self.object.pk})
    
class PacienteDetailView(DetailView):
    model = Paciente
    template_name = "paciente/detalle.html"
    context_object_name = "paciente"

class PacienteUpdateView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "paciente/crear_paciente.html"

    def get_success_url(self):
        return reverse_lazy("paciente:detalle_paciente", kwargs={"pk": self.object.pk})

class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = "paciente/confirmar_eliminar.html"
    success_url = reverse_lazy("paciente:lista_paciente")
