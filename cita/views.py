from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from .models import Cita
from .forms import CitaForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from acceso.models import UsuarioRol, UsuarioHospital
from acceso.mixins import PermisoMedicoMixin, PermisoAltoMixin


class CitaListView(LoginRequiredMixin, PermisoMedicoMixin, ListView):
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

        user = self.request.user

        # Si el usuario NO es director → limitar al hospital asignado
        if not UsuarioRol.objects.filter(
            usuario=user, rol__nombre="DIRECCIÓN"
        ).exists():
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if hospital_usuario:
                qs = qs.filter(hospital=hospital_usuario.hospital)
            else:
                return qs.none()

        # Filtros adicionales
        if paciente_id:
            qs = qs.filter(paciente_id=paciente_id)
        if medico_id:
            qs = qs.filter(medico_id=medico_id)
        if estado:
            qs = qs.filter(estado=estado)
        if fecha:
            qs = qs.filter(fecha=fecha)
        if (
            hospital_id
            and UsuarioRol.objects.filter(
                usuario=user, rol__nombre="DIRECCIÓN"
            ).exists()
        ):
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


class CitaDetailView(LoginRequiredMixin, PermisoMedicoMixin, DetailView):
    model = Cita
    template_name = "cita/detalle.html"
    context_object_name = "cita"


class CitaCreateView(LoginRequiredMixin, PermisoMedicoMixin, CreateView):
    model = Cita
    form_class = CitaForm
    template_name = "cita/formulario.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        cita = form.save(commit=False)
        user = self.request.user

        # Si no es director → hospital fijo
        if not UsuarioRol.objects.filter(
            usuario=user, rol__nombre="DIRECCIÓN"
        ).exists():
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if hospital_usuario:
                cita.hospital = hospital_usuario.hospital
            else:
                raise PermissionDenied("No tienes hospital asignado.")

        cita.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cita:detalle_cita", kwargs={"pk": self.object.pk})

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


class CitaUpdateView(LoginRequiredMixin, PermisoMedicoMixin, UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = "cita/formulario.html"

    def dispatch(self, request, *args, **kwargs):
        cita = self.get_object()
        user = request.user
        if not UsuarioRol.objects.filter(
            usuario=user, rol__nombre="DIRECCIÓN"
        ).exists():
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if not hospital_usuario or cita.hospital != hospital_usuario.hospital:
                raise PermissionDenied("No puedes editar citas de otro hospital.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("cita:detalle_cita", kwargs={"pk": self.object.pk})

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


class CitaDeleteView(LoginRequiredMixin, PermisoAltoMixin, DeleteView):
    model = Cita
    template_name = "cita/confirmar_eliminar.html"
    success_url = reverse_lazy("cita:lista_cita")

    def dispatch(self, request, *args, **kwargs):
        cita = self.get_object()
        user = request.user
        if not UsuarioRol.objects.filter(
            usuario=user, rol__nombre="DIRECCIÓN"
        ).exists():
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if not hospital_usuario or cita.hospital != hospital_usuario.hospital:
                raise PermissionDenied("No puedes editar citas de otro hospital.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("cita:detalle_cita", kwargs={"pk": self.object.pk})


class CitaCalendarioView(LoginRequiredMixin, PermisoMedicoMixin, TemplateView):
    template_name = "cita/calendario.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.localdate()
        user = self.request.user

        qs = Cita.objects.select_related("hospital", "paciente", "medico").filter(
            fecha__gte=hoy
        )

        if not UsuarioRol.objects.filter(
            usuario=user, rol__nombre="DIRECCIÓN"
        ).exists():
            hospital_usuario = UsuarioHospital.objects.filter(usuario=user).first()
            if hospital_usuario:
                qs = qs.filter(hospital=hospital_usuario.hospital)
            else:
                qs = qs.none()

        ctx["hoy"] = hoy
        ctx["proximas"] = qs.order_by("fecha", "hora")[:50]
        return ctx
