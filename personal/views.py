from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Medico, Enfermero, Personal
from .forms import MedicoForm, EnfermeroForm, PersonalForm
from django.contrib.auth.mixins import LoginRequiredMixin
from acceso.mixins import PermisoAltoMixin, PermisoMedicoMixin
from acceso.access import HospitalAccessMixin, visibles_para

# -----------------------
# MÉDICOS
# -----------------------


class MedicoListView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, ListView
):
    model = Medico
    template_name = "medicos/medico_list.html"
    context_object_name = "medicos"

    def get_queryset(self):
        return visibles_para(Medico, self.request.user).select_related("hospital")


class MedicoCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = "medicos/medico_form.html"
    success_url = reverse_lazy("personal:medico_list")


class MedicoUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = "medicos/medico_form.html"
    success_url = reverse_lazy("personal:medico_list")


class MedicoDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Medico
    template_name = "medicos/medico_confirm_delete.html"
    success_url = reverse_lazy("personal:medico_list")


# -----------------------
# ENFERMEROS
# -----------------------


class EnfermeroListView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, ListView
):
    model = Enfermero
    template_name = "enfermeros/enfermero_list.html"
    context_object_name = "enfermeros"

    def get_queryset(self):
        return visibles_para(Enfermero, self.request.user).select_related("hospital")


class EnfermeroCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = Enfermero
    form_class = EnfermeroForm
    template_name = "enfermeros/enfermero_form.html"
    success_url = reverse_lazy("personal:enfermero_list")


class EnfermeroUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = Enfermero
    form_class = EnfermeroForm
    template_name = "enfermeros/enfermero_form.html"
    success_url = reverse_lazy("personal:enfermero_list")


class EnfermeroDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Enfermero
    template_name = "enfermeros/enfermero_confirm_delete.html"
    success_url = reverse_lazy("personal:enfermero_list")


# CRUD genérico para Personal
class PersonalListView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, ListView
):
    model = Personal
    template_name = "personal/personal_list.html"
    context_object_name = "personal"

    def get_queryset(self):
        qs = visibles_para(Personal, self.request.user).select_related("hospital")
        area = self.kwargs.get("area")
        if area:
            qs = qs.filter(area=area)
        return qs


class PersonalCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = Personal
    form_class = PersonalForm
    template_name = "personal/personal_form.html"
    success_url = reverse_lazy("personal:personal_list")


class PersonalUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = Personal
    form_class = PersonalForm
    template_name = "personal/personal_form.html"
    success_url = reverse_lazy("personal:personal_list")


class PersonalDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Personal
    template_name = "personal/personal_confirm_delete.html"
    success_url = reverse_lazy("personal:personal_list")
