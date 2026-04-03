from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Medico, Enfermero
from .forms import MedicoForm, EnfermeroForm
from django.contrib.auth.mixins import LoginRequiredMixin


# -----------------------
# MÉDICOS
# -----------------------

class MedicoListView(LoginRequiredMixin, ListView):
    model = Medico
    template_name = "medicos/medico_list.html"
    context_object_name = "medicos"


class MedicoCreateView(LoginRequiredMixin, CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = "medicos/medico_form.html"
    success_url = reverse_lazy("personal:medico_list")


class MedicoUpdateView(LoginRequiredMixin,UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = "medicos/medico_form.html"
    success_url = reverse_lazy("personal:medico_list")


class MedicoDeleteView(LoginRequiredMixin, DeleteView):
    model = Medico
    template_name = "medicos/medico_confirm_delete.html"
    success_url = reverse_lazy("personal:medico_list")


# -----------------------
# ENFERMEROS
# -----------------------

class EnfermeroListView(LoginRequiredMixin, ListView):
    model = Enfermero
    template_name = "enfermeros/enfermero_list.html"
    context_object_name = "enfermeros"


class EnfermeroCreateView(LoginRequiredMixin, CreateView):
    model = Enfermero
    form_class = EnfermeroForm
    template_name = "enfermeros/enfermero_form.html"
    success_url = reverse_lazy("personal:enfermero_list")


class EnfermeroUpdateView(LoginRequiredMixin, UpdateView):
    model = Enfermero
    form_class = EnfermeroForm
    template_name = "enfermeros/enfermero_form.html"
    success_url = reverse_lazy("personal:enfermero_list")


class EnfermeroDeleteView(LoginRequiredMixin, DeleteView):
    model = Enfermero
    template_name = "enfermeros/enfermero_confirm_delete.html"
    success_url = reverse_lazy("personal:enfermero_list")