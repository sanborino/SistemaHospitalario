from django.views.generic import ListView, DetailView
from .models import Auditoria
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from acceso.mixins import PermisoAltoMixin
from django.views.generic import ListView
from .models import Auditoria
from acceso.access import HospitalAccessMixin, visibles_para


class AuditoriaListView(
    LoginRequiredMixin, PermisoAltoMixin, HospitalAccessMixin, ListView
):
    model = Auditoria
    template_name = "auditoria/auditoria_list.html"
    ordering = ["-fecha"]
    paginate_by = 10

    def get_queryset(self):
        qs = visibles_para(Auditoria, self.request.user)

        # 🔹 Si visibles_para devolvió None, forzamos queryset vacío
        if qs is None:
            qs = Auditoria.objects.none()

        # 🔹 Si tu modelo Auditoria no tiene hospital/usuario, quita select_related
        # qs = qs.select_related("hospital", "usuario")  # solo si existen esos campos

        fecha_desde = self.request.GET.get("desde")
        fecha_hasta = self.request.GET.get("hasta")

        # 🔹 Filtro por rango de fechas
        if fecha_desde and fecha_hasta:
            qs = qs.filter(fecha__range=[fecha_desde, fecha_hasta])
        elif fecha_desde:
            qs = qs.filter(fecha__gte=fecha_desde)
        elif fecha_hasta:
            qs = qs.filter(fecha__lte=fecha_hasta)
        return qs.order_by("-fecha")


class AuditoriaDetailView(
    LoginRequiredMixin, PermisoAltoMixin, HospitalAccessMixin, DetailView
):
    model = Auditoria
    template_name = "auditoria/auditoria_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tabla = self.object.tabla
        registro_id = self.object.registro_id

        Modelo = None
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                if model._meta.db_table == tabla:
                    Modelo = model
                    break
            if Modelo:
                break

        registro_original = None
        campos = {}

        if Modelo:
            pk_name = Modelo._meta.pk.name
            registro_original = (
                visibles_para(Modelo, self.request.user)
                .filter(**{pk_name: registro_id})
                .first()
            )

            if registro_original:
                for field in registro_original._meta.get_fields():
                    if field.is_relation and (
                        field.one_to_many
                        or field.many_to_many
                        or (field.one_to_one and field.auto_created)
                    ):
                        continue
                    nombre = field.verbose_name
                    valor = getattr(registro_original, field.name, None)
                    campos[nombre] = valor

        context["registro_original"] = registro_original
        context["campos"] = campos
        return context
