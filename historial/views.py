from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import HistorialClinico
from .forms import HistorialClinicoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from acceso.models import UsuarioRol, UsuarioHospital
from django.shortcuts import redirect
from acceso.mixins import PermisoMedicoMixin, PermisoAltoMixin


class HistorialListView(LoginRequiredMixin, PermisoMedicoMixin, ListView):
    model = HistorialClinico
    template_name = "historial/lista.html"
    context_object_name = "historiales"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("hospital", "paciente", "medico")
            .order_by("-fecha", "-id")
        )

        paciente_id = self.request.GET.get("paciente")
        hospital_id = self.request.GET.get("hospital")

        user = self.request.user

        # Si el usuario NO es director → limitar al hospital asignado
        if not UsuarioRol.objects.filter(
            usuario=user, rol__nombre="DIRECCION"
        ).exists():
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if hospital_usuario:
                qs = qs.filter(hospital=hospital_usuario.hospital)
            else:
                return qs.none()  # usuario sin hospital asignado

        # Filtros adicionales
        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)
        if hospital_id:
            qs = qs.filter(hospital_id=hospital_id)

        return qs

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


class HistorialDetailView(LoginRequiredMixin, PermisoMedicoMixin, DetailView):
    model = HistorialClinico
    template_name = "historial/detalle.html"
    context_object_name = "historial"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Si es director → acceso global
        if UsuarioRol.objects.filter(usuario=user, rol__nombre="DIRECCIÓN").exists():
            context["es_director"] = True
        else:
            # Usuario normal → mostrar solo su hospital
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if hospital_usuario:
                context["hospital_nombre"] = hospital_usuario.hospital.nombre
        return context


class HistorialCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = HistorialClinico
    form_class = HistorialClinicoForm
    template_name = "historial/formulario.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # 👈 pasar el usuario al formulario
        return kwargs

    def form_valid(self, form):
        historial = form.save(commit=False)
        user = self.request.user

        # Refuerzo de seguridad: si no es director, forzar hospital correcto
        if not UsuarioRol.objects.filter(
            usuario=user, rol__nombre="DIRECCIÓN"
        ).exists():
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if hospital_usuario:
                historial.hospital = hospital_usuario.hospital

        historial.save()

        # Si hay cita asociada, marcarla como atendida
        if historial.cita:
            historial.cita.estado = "atendida"
            historial.cita.save(update_fields=["estado"])

        return redirect(self.get_success_url())

    def get_initial(self):
        initial = super().get_initial()
        cita_id = self.request.GET.get("cita")

        if cita_id:
            from cita.models import Cita

            c = Cita.objects.select_related("hospital", "paciente", "medico").get(
                pk=cita_id
            )
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Si es director → puede elegir hospital
        if UsuarioRol.objects.filter(usuario=user, rol__nombre="DIRECCIÓN").exists():
            context["es_director"] = True
        else:
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if hospital_usuario:
                context["hospital_nombre"] = hospital_usuario.hospital.nombre
        return context

    def get_success_url(self):
        return reverse_lazy(
            "historial:detalle_historial", kwargs={"pk": self.object.pk}
        )


class HistorialUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = HistorialClinico
    form_class = HistorialClinicoForm
    template_name = "historial/formulario.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # 👈 pasar el usuario al formulario
        return kwargs

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

    def get_success_url(self):
        return reverse_lazy(
            "historial:detalle_historial", kwargs={"pk": self.object.pk}
        )


class HistorialDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = HistorialClinico
    template_name = "historial/confirmar_eliminar.html"
    success_url = reverse_lazy("historial:lista_historial")
