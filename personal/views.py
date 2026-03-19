from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Medico, Enfermero
from .forms import MedicoForm, EnfermeroForm

# -----------------------
# MÉDICOS
# -----------------------

class MedicoListView(ListView):
    model = Medico
    template_name = "medicos/medico_list.html"
    context_object_name = "medicos"


class MedicoCreateView(CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = "medicos/medico_form.html"
    success_url = reverse_lazy("personal:medico_list")


class MedicoUpdateView(UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = "medicos/medico_form.html"
    success_url = reverse_lazy("personal:medico_list")


class MedicoDeleteView(DeleteView):
    model = Medico
    template_name = "medicos/medico_confirm_delete.html"
    success_url = reverse_lazy("personal:medico_list")


# -----------------------
# ENFERMEROS
# -----------------------

class EnfermeroListView(ListView):
    model = Enfermero
    template_name = "enfermeros/enfermero_list.html"
    context_object_name = "enfermeros"


class EnfermeroCreateView(CreateView):
    model = Enfermero
    form_class = EnfermeroForm
    template_name = "enfermeros/enfermero_form.html"
    success_url = reverse_lazy("personal:enfermero_list")


class EnfermeroUpdateView(UpdateView):
    model = Enfermero
    form_class = EnfermeroForm
    template_name = "enfermeros/enfermero_form.html"
    success_url = reverse_lazy("personal:enfermero_list")


class EnfermeroDeleteView(DeleteView):
    model = Enfermero
    template_name = "enfermeros/enfermero_confirm_delete.html"
    success_url = reverse_lazy("personal:enfermero_list")