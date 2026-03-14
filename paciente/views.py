from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Paciente
from .forms import PacienteForm
from django.contrib.auth.mixins import LoginRequiredMixin


class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = "lista_pacientes.html"
    context_object_name = "pacientes"

class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "crear_paciente.html"
    success_url = reverse_lazy("paciente:lista_pacientes")
