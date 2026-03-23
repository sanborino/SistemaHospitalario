from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Factura, FacturaDetalle, Pago
from .forms import FacturaForm, FacturaDetalleForm, PagoForm
from paciente.models import Paciente
from hospital.models import Hospital
from .models import Factura, FacturaDetalle, Pago, Cargo

# ---------------- FACTURAS ----------------


def factura_lista(request):
    estado = request.GET.get("estado", "PENDIENTE")
    origen = request.GET.get("origen", "todos")

    facturas = Factura.objects.all()

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


def factura_crear(request):
    form = FacturaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("facturacion:factura_lista")
    return render(request, "facturacion/form.html", {"form": form})


def factura_editar(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    form = FacturaForm(request.POST or None, instance=factura)
    if form.is_valid():
        form.save()
        return redirect("facturacion:factura_lista")
    return render(request, "facturacion/form.html", {"form": form})


def factura_detalle(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    detalles = FacturaDetalle.objects.filter(factura=factura)
    pagos = Pago.objects.filter(factura=factura)

    # Calcular subtotal por detalle
    subtotal_detalles = sum(d.cantidad * d.precio_unitario for d in detalles)

    # Total pagado
    total_pagado = sum(p.monto for p in pagos)

    # Saldo pendiente
    saldo = factura.total - total_pagado

    # Si ya se pagó el total, cambiar estado a PAGADA
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


class FacturaDeleteView(DeleteView):
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


def detalle_crear(request):
    form = FacturaDetalleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("facturacion:factura_lista")
    return render(request, "facturacion/form_detalle.html", {"form": form})


def detalle_editar(request, pk):
    detalle = get_object_or_404(FacturaDetalle, pk=pk)
    form = FacturaDetalleForm(request.POST or None, instance=detalle)
    if form.is_valid():
        form.save()
        return redirect("facturacion:factura_lista")
    return render(request, "facturacion/form_detalle.html", {"form": form})


def detalle_eliminar(request, pk):
    detalle = get_object_or_404(FacturaDetalle, pk=pk)
    detalle.delete()
    return redirect("facturacion:factura_lista")


# ---------------- PAGOS ----------------


def pago_crear(request):
    form = PagoForm(request.POST or None)
    if form.is_valid():
        pago = form.save()

        # Recalcular total pagado
        factura = pago.factura
        total_pagado = sum(p.monto for p in Pago.objects.filter(factura=factura))

        # Cambiar estado si ya está pagada
        if total_pagado >= factura.total:
            factura.estado = "PAGADA"
            factura.save()

        return redirect("facturacion:factura_detalle", pk=factura.id)

    return render(request, "facturacion/form_pago.html", {"form": form})


def pago_editar(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    form = PagoForm(request.POST or None, instance=pago)
    if form.is_valid():
        form.save()
        return redirect("facturacion:factura_lista")
    return render(request, "facturacion/form_pago.html", {"form": form})


def pago_eliminar(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    pago.delete()
    return redirect("facturacion:factura_lista")


def generar_factura_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)

    # aquí puedes ajustar cómo obtienes el hospital (por usuario logueado, por selección, etc.)
    hospital = paciente.hospital

    cargos = Cargo.objects.filter(paciente=paciente, facturado=False)

    if not cargos.exists():
        messages.warning(request, "No hay cargos pendientes para este paciente.")
        return redirect("facturacion:factura_lista")

    factura = Factura.objects.create(
        paciente=paciente,
        hospital=hospital,
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
