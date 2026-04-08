from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Urgencia, AtencionUrgencia, AltaUrgencia
from .forms import UrgenciaForm, AtencionUrgenciaForm, AltaUrgenciaForm
from facturacion.models import Cargo
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from acceso.mixins import permiso_medico_required
from acceso.mixins import PermisoMedicoMixin, PermisoAltoMixin
from acceso.models import UsuarioRol, UsuarioHospital


# CRUD Urgencia
class UrgenciaListView(LoginRequiredMixin, PermisoMedicoMixin, ListView):
    model = Urgencia
    template_name = "urgencia/urgencia_lista.html"
    context_object_name = "urgencias"
    paginate_by = 10
    ordering = ["-fecha_ingreso"]


class UrgenciaDetailView(LoginRequiredMixin, PermisoMedicoMixin, DetailView):
    model = Urgencia
    template_name = "urgencia/urgencia_detalle.html"
    context_object_name = "urgencia"


class UrgenciaCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = Urgencia
    form_class = UrgenciaForm
    template_name = "urgencia/urgencia_formulario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if UsuarioRol.objects.filter(usuario=user, rol__nombre="DIRECCIÓN").exists():
            context["es_director"] = True
        else:
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if hospital_usuario:
                context["hospital_nombre"] = hospital_usuario.hospital.nombre
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # 👈 pasamos el usuario al form
        return kwargs

    def form_valid(self, form):
        # Asignar hospital automáticamente si no es director
        if not UsuarioRol.objects.filter(
            usuario=self.request.user, rol__nombre="DIRECCIÓN"
        ).exists():
            hospital_usuario = UsuarioHospital.objects.filter(
                usuario=self.request.user
            ).first()
            if hospital_usuario:
                form.instance.hospital = hospital_usuario.hospital
        return super().form_valid(form)


class UrgenciaUpdateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = Urgencia
    form_class = UrgenciaForm
    template_name = "urgencia/urgencia_formulario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if UsuarioRol.objects.filter(usuario=user, rol__nombre="DIRECCIÓN").exists():
            context["es_director"] = True
        else:
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if hospital_usuario:
                context["hospital_nombre"] = hospital_usuario.hospital.nombre
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # 👈 pasamos el usuario al form
        return kwargs

    def form_valid(self, form):
        # Asignar hospital automáticamente si no es director
        if not UsuarioRol.objects.filter(
            usuario=self.request.user, rol__nombre="DIRECCIÓN"
        ).exists():
            hospital_usuario = UsuarioHospital.objects.filter(
                usuario=self.request.user
            ).first()
            if hospital_usuario:
                form.instance.hospital = hospital_usuario.hospital
        return super().form_valid(form)


class UrgenciaDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Urgencia
    template_name = "urgencia/urgencia_confirmar_eliminar.html"
    success_url = reverse_lazy("urgencia:lista_urgencia")


# CRUD AtencionUrgencia
class AtencionUrgenciaListView(LoginRequiredMixin, PermisoMedicoMixin, ListView):
    model = AtencionUrgencia
    template_name = "urgencia/atencion_lista.html"
    context_object_name = "atenciones"
    paginate_by = 10
    ordering = ["-fecha"]

    def get_queryset(self):
        return super().get_queryset().select_related("urgencia", "medico")


class AtencionUrgenciaDetailView(LoginRequiredMixin, PermisoMedicoMixin, DetailView):
    model = AtencionUrgencia
    template_name = "urgencia/atencion_detalle.html"
    context_object_name = "atencion"


class AtencionUrgenciaCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = AtencionUrgencia
    form_class = AtencionUrgenciaForm
    template_name = "urgencia/atencion_formulario.html"

    def get_success_url(self):
        return reverse_lazy("urgencia:detalle_atencion", kwargs={"pk": self.object.pk})


class AtencionUrgenciaUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = AtencionUrgencia
    form_class = AtencionUrgenciaForm
    template_name = "urgencia/atencion_formulario.html"

    def get_success_url(self):
        return reverse_lazy("urgencia:detalle_atencion", kwargs={"pk": self.object.pk})


class AtencionUrgenciaDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = AtencionUrgencia
    template_name = "urgencia/atencion_confirmar_eliminar.html"
    context_object_name = "atencion"
    success_url = reverse_lazy("urgencia:lista_atencion")


# CRUD AltaUrgencia
class AltaUrgenciaListView(LoginRequiredMixin, PermisoMedicoMixin, ListView):
    model = AltaUrgencia
    template_name = "urgencia/alta_lista.html"
    context_object_name = "altas"
    paginate_by = 10
    ordering = ["-fecha"]

    def get_queryset(self):
        return super().get_queryset().select_related("urgencia")


class AltaUrgenciaDetailView(LoginRequiredMixin, PermisoMedicoMixin, DetailView):
    model = AltaUrgencia
    template_name = "urgencia/alta_detalle.html"
    context_object_name = "alta"


class AltaUrgenciaCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = AltaUrgencia
    form_class = AltaUrgenciaForm
    template_name = "urgencia/alta_formulario.html"

    def get_success_url(self):
        return reverse_lazy("urgencia:detalle_alta", kwargs={"pk": self.object.pk})


class AltaUrgenciaUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = AltaUrgencia
    form_class = AltaUrgenciaForm
    template_name = "urgencia/alta_formulario.html"

    def get_success_url(self):
        return reverse_lazy("urgencia:detalle_alta", kwargs={"pk": self.object.pk})


class AltaUrgenciaDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = AltaUrgencia
    template_name = "urgencia/alta_confirmar_eliminar.html"
    context_object_name = "alta"
    success_url = reverse_lazy("urgencia:lista_alta")


@permiso_medico_required
def cerrar_urgencia(request, id):
    urgencia = get_object_or_404(Urgencia, pk=id)

    Cargo.objects.create(
        paciente=urgencia.paciente,
        descripcion="Atención de urgencias",
        cantidad=1,
        precio_unitario=500,  # tu tarifa
        urgencia=urgencia,
    )

    urgencia.estado = "CERRADO"
    urgencia.save()

    messages.success(request, "Urgencia cerrada y cargo generado.")
    return redirect("urgencia:detalle", id)
