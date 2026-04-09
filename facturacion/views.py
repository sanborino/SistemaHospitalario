from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
)
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Factura, FacturaDetalle, Pago
from .forms import FacturaForm, FacturaDetalleForm, PagoForm
from paciente.models import Paciente
from .models import Factura, FacturaDetalle, Pago, Cargo
from acceso.mixins import permiso_admin_required, permiso_alto_required
from acceso.mixins import PermisoAltoMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from acceso.access import visibles_para
from acceso.access import HospitalAccessMixin

# ---------------- FACTURAS ----------------


@permiso_admin_required
def factura_lista(request):
    estado = request.GET.get("estado", "PENDIENTE")
    origen = request.GET.get("origen", "todos")

    facturas = visibles_para(Factura, request.user)

    if estado != "todos":
        facturas = facturas.filter(estado=estado)

    if origen == "laboratorio":
        facturas = facturas.filter(origen_estudio=True)
    elif origen == "manual":
        facturas = facturas.filter(origen_estudio=False)

    estados = [
        ("PENDIENTE", "Pendiente"),
        ("PAGADA", "Pagada"),
        ("ANULADA", "Anulada"),
        ("EN_PROCESO", "En proceso"),
    ]

    origenes = [
        ("todos", "Todas"),
        ("laboratorio", "De laboratorio"),
        ("manual", "Manuales"),
    ]

    return render(
        request,
        "facturacion/lista.html",
        {
            "facturas": facturas,
            "estado_seleccionado": estado,
            "origen_seleccionado": origen,
            "estados": estados,
            "origenes": origenes,
        },
    )


@permiso_admin_required
def factura_crear(request):
    form = FacturaForm(request.POST or None, user=request.user)

    if form.is_valid():
        factura = form.save(commit=False)
        # hospital ya se asigna/oculta en el formulario
        factura.save()
        return redirect("facturacion:factura_lista")

    return render(request, "facturacion/form.html", {"form": form})


from acceso.access import visibles_para


@permiso_admin_required
def factura_editar(request, pk):
    # 🔑 Filtrar facturas por hospital del usuario
    factura = get_object_or_404(visibles_para(Factura, request.user), pk=pk)

    form = FacturaForm(request.POST or None, instance=factura, user=request.user)

    if form.is_valid():
        factura = form.save(commit=False)
        # hospital ya se controla en el formulario con filtrar_queryset
        factura.save()
        return redirect("facturacion:factura_lista")

    return render(request, "facturacion/form.html", {"form": form})


@permiso_admin_required
def factura_detalle(request, pk):
    factura = get_object_or_404(visibles_para(Factura, request.user), pk=pk)
    detalles = FacturaDetalle.objects.filter(factura=factura)
    pagos = Pago.objects.filter(factura=factura)

    subtotal_detalles = sum(d.cantidad * d.precio_unitario for d in detalles)
    total_pagado = sum(p.monto for p in pagos)
    saldo = subtotal_detalles - total_pagado

    if saldo <= 0 and factura.estado != "PAGADA":
        factura.estado = "PAGADA"
        factura.save()

    return render(
        request,
        "facturacion/detalle_factura.html",
        {
            "factura": factura,
            "detalles": detalles,
            "pagos": pagos,
            "subtotal_detalles": subtotal_detalles,
            "total_pagado": total_pagado,
            "saldo": saldo,
        },
    )


class FacturaDeleteView(
    LoginRequiredMixin, PermisoAltoMixin, HospitalAccessMixin, DeleteView
):
    model = Factura
    template_name = "facturacion/factura_confirmar_eliminar.html"
    success_url = reverse_lazy("facturacion:factura_lista")

    def delete(self, request, *args, **kwargs):
        factura = self.get_object()
        if factura.estado == "PAGADA":
            messages.error(request, "No se puede eliminar una factura pagada.")
            return redirect("facturacion:factura_lista")
        return super().delete(request, *args, **kwargs)


# ---------------- DETALLES ----------------


@permiso_admin_required
def detalle_crear(request):
    form = FacturaDetalleForm(request.POST or None, user=request.user)
    if form.is_valid():
        detalle = form.save(commit=False)
        # 🔑 Validar que la factura pertenece al hospital del usuario
        if detalle.factura not in visibles_para(Factura, request.user):
            messages.error(
                request, "No puedes agregar detalles a facturas de otro hospital."
            )
            return redirect("facturacion:factura_lista")
        detalle.save()
        return redirect("facturacion:factura_lista")
    return render(request, "facturacion/form_detalle.html", {"form": form})


@permiso_admin_required
def detalle_editar(request, pk):
    detalle = get_object_or_404(FacturaDetalle, pk=pk)
    # 🔑 Validar que la factura pertenece al hospital del usuario
    if detalle.factura not in visibles_para(Factura, request.user):
        return redirect("facturacion:factura_lista")

    form = FacturaDetalleForm(request.POST or None, instance=detalle, user=request.user)
    if form.is_valid():
        form.save()
        return redirect("facturacion:factura_lista")
    return render(request, "facturacion/form_detalle.html", {"form": form})


from acceso.access import visibles_para


@permiso_alto_required
def detalle_eliminar(request, pk):
    detalle = get_object_or_404(FacturaDetalle, pk=pk)

    # 🔑 Validar que la factura asociada pertenece al hospital del usuario
    if detalle.factura not in visibles_para(Factura, request.user):
        messages.error(
            request, "No puedes eliminar detalles de facturas de otro hospital."
        )
        return redirect("facturacion:factura_lista")

    detalle.delete()
    messages.success(request, "Detalle eliminado correctamente.")
    return redirect("facturacion:factura_lista")


# ---------------- PAGOS ----------------


@permiso_admin_required
def pago_crear(request):
    form = PagoForm(request.POST or None, user=request.user)
    if form.is_valid():
        pago = form.save(commit=False)
        # 🔑 Validar que la factura pertenece al hospital del usuario
        if pago.factura not in visibles_para(Factura, request.user):
            messages.error(
                request, "No puedes registrar pagos en facturas de otro hospital."
            )
            return redirect("facturacion:factura_lista")
        pago.save()

        # Recalcular total pagado
        factura = pago.factura
        total_pagado = sum(p.monto for p in Pago.objects.filter(factura=factura))
        if total_pagado >= factura.total:
            factura.estado = "PAGADA"
            factura.save()

        return redirect("facturacion:factura_detalle", pk=factura.id)

    return render(request, "facturacion/form_pago.html", {"form": form})


@permiso_admin_required
def pago_editar(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    # 🔑 Validar que la factura pertenece al hospital del usuario
    if pago.factura not in visibles_para(Factura, request.user):
        return redirect("facturacion:factura_lista")

    form = PagoForm(request.POST or None, instance=pago, user=request.user)
    if form.is_valid():
        form.save()
        return redirect("facturacion:factura_lista")
    return render(request, "facturacion/form_pago.html", {"form": form})


from acceso.access import visibles_para


@permiso_alto_required
def pago_eliminar(request, pk):
    pago = get_object_or_404(Pago, pk=pk)

    # 🔑 Validar que la factura asociada pertenece al hospital del usuario
    if pago.factura not in visibles_para(Factura, request.user):
        messages.error(
            request, "No puedes eliminar pagos de facturas de otro hospital."
        )
        return redirect("facturacion:factura_lista")

    factura_id = pago.factura.id
    pago.delete()
    messages.success(request, "Pago eliminado correctamente.")
    return redirect("facturacion:factura_detalle", pk=factura_id)


from acceso.access import visibles_para


@permiso_admin_required
def generar_factura_paciente(request, paciente_id):
    # 🔑 Validar que el paciente pertenece al hospital del usuario
    paciente = get_object_or_404(visibles_para(Paciente, request.user), pk=paciente_id)

    cargos = Cargo.objects.filter(paciente=paciente, facturado=False)

    if not cargos.exists():
        messages.warning(request, "No hay cargos pendientes para este paciente.")
        return redirect("facturacion:factura_lista")

    factura = Factura.objects.create(
        paciente=paciente,
        hospital=paciente.hospital,  # hospital ya validado
        total=0,
        estado="PENDIENTE",
    )

    total = 0
    for cargo in cargos:
        FacturaDetalle.objects.create(
            factura=factura,
            descripcion=cargo.descripcion,
            cantidad=cargo.cantidad,
            precio_unitario=cargo.precio_unitario,
        )
        total += cargo.subtotal()
        cargo.facturado = True
        cargo.factura = factura
        cargo.save()

    factura.total = total
    factura.save()

    messages.success(request, f"Factura #{factura.id} generada para {paciente}.")
    return redirect("facturacion:factura_detalle", pk=factura.id)
