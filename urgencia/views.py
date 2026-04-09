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
from acceso.access import HospitalAccessMixin, visibles_para

# CRUD Urgencia


class UrgenciaListView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, ListView
):
    model = Urgencia
    template_name = "urgencia/urgencia_lista.html"
    context_object_name = "urgencias"
    paginate_by = 10
    ordering = ["-fecha_ingreso"]

    def get_queryset(self):
        # Mostrar solo urgencias pendientes (sin atención aún)
        return visibles_para(Urgencia, self.request.user).exclude(
            estado__in=["EN_ATENCION", "DADO_DE_ALTA", "CERRADO"]
        )


class UrgenciaDetailView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, DetailView
):
    model = Urgencia
    template_name = "urgencia/urgencia_detalle.html"
    context_object_name = "urgencia"


class UrgenciaCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = Urgencia
    form_class = UrgenciaForm
    template_name = "urgencia/urgencia_formulario.html"

    def get_success_url(self):
        return reverse_lazy("urgencia:detalle_urgencia", kwargs={"pk": self.object.pk})

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


class UrgenciaUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = Urgencia
    form_class = UrgenciaForm
    template_name = "urgencia/urgencia_formulario.html"

    def get_success_url(self):
        return reverse_lazy("urgencia:detalle_urgencia", kwargs={"pk": self.object.pk})

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
class AtencionUrgenciaListView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, ListView
):
    model = AtencionUrgencia
    template_name = "urgencia/atencion_lista.html"
    context_object_name = "atenciones"
    paginate_by = 10
    ordering = ["-fecha"]

    def get_queryset(self):
        # Mostrar solo urgencias en atención (estado EN_ATENCION)
        return (
            visibles_para(AtencionUrgencia, self.request.user)
            .select_related("urgencia", "medico")
            .filter(urgencia__estado="EN_ATENCION")
        )


class AtencionUrgenciaDetailView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, DetailView
):
    model = AtencionUrgencia
    template_name = "urgencia/atencion_detalle.html"
    context_object_name = "atencion"


class AtencionUrgenciaCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = AtencionUrgencia
    form_class = AtencionUrgenciaForm
    template_name = "urgencia/atencion_formulario.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

        # Cambiar estado de urgencia a EN_ATENCION
        atencion.save()

        urgencia.estado = "EN_ATENCION"
        urgencia.save()

        messages.success(self.request, "Atención registrada correctamente.")
        return redirect("urgencia:detalle_atencion", pk=atencion.pk)

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
class AltaUrgenciaListView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, ListView
):
    model = AltaUrgencia
    template_name = "urgencia/alta_lista.html"
    context_object_name = "altas"
    paginate_by = 10
    ordering = ["-fecha"]

    def get_queryset(self):
        # Mostrar solo urgencias dadas de alta
        return (
            visibles_para(AltaUrgencia, self.request.user)
            .select_related("urgencia")
            .filter(urgencia__estado="DADO_DE_ALTA")
        )


class AltaUrgenciaDetailView(
    LoginRequiredMixin, PermisoMedicoMixin, HospitalAccessMixin, DetailView
):
    model = AltaUrgencia
    template_name = "urgencia/alta_detalle.html"
    context_object_name = "alta"


class AltaUrgenciaCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = AltaUrgencia
    form_class = AltaUrgenciaForm
    template_name = "urgencia/alta_formulario.html"

    def form_valid(self, form):
        # Obtener la urgencia del formulario limpio
        alta = form.save(commit=False)
        urgencia = alta.urgencia

        # Validar que no haya un alta previo para esta urgencia
        if AltaUrgencia.objects.filter(urgencia=urgencia).exists():
            messages.error(self.request, "Esta urgencia ya fue dada de alta.")
            return redirect("urgencia:detalle_urgencia", pk=urgencia.pk)

        # Guardar el alta y cambiar estado de urgencia
        alta.save()
        urgencia.estado = "DADO_DE_ALTA"
        urgencia.save()

        messages.success(self.request, "Urgencia dada de alta correctamente.")
        return redirect("urgencia:detalle_alta", pk=alta.pk)

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
    urgencia = get_object_or_404(visibles_para(Urgencia, request.user), pk=id)

    Cargo.objects.create(
        paciente=urgencia.paciente,
        descripcion="Atención de urgencias",
        cantidad=1,
        precio_unitario=500,
        urgencia=urgencia,
    )

    urgencia.estado = "CERRADO"
    urgencia.save()

    messages.success(request, "Urgencia cerrada y cargo generado.")
    return redirect("urgencia:detalle", id)
