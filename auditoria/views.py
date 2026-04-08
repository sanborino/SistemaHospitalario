from django.views.generic import ListView, DetailView
from .models import Auditoria
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from acceso.mixins import PermisoAltoMixin
from django.views.generic import ListView
from .models import Auditoria


class AuditoriaListView(LoginRequiredMixin, PermisoAltoMixin, ListView):
    model = Auditoria
    template_name = "auditoria/auditoria_list.html"
    ordering = ["-fecha"]  # más reciente primero
    paginate_by = 10  # 10 registros por página

    def get_queryset(self):
        queryset = super().get_queryset()
        fecha = self.request.GET.get("fecha", None)
        if fecha:
            queryset = queryset.filter(fecha__date=fecha)
        return queryset


class AuditoriaDetailView(LoginRequiredMixin, PermisoAltoMixin, DetailView):
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
            registro_original = Modelo.objects.filter(**{pk_name: registro_id}).first()

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
