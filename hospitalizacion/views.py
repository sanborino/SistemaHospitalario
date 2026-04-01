from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from infraestructura.models import Cama
from .models import AsignacionCama
from .utils import cama_disponible, paciente_con_cama_activa
from paciente.models import Paciente
from facturacion.models import Cargo


from facturacion.models import Cargo


def asignar_cama(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    camas = Cama.objects.filter(estado="DISPONIBLE")

    if request.method == "POST":
        cama_id = request.POST.get("cama_id")
        cama = get_object_or_404(Cama, id=cama_id)

        if paciente_con_cama_activa(paciente):
            messages.error(request, "El paciente ya tiene una cama asignada.")
            return redirect("paciente:detalle_paciente", paciente_id=paciente.id)

        if not cama_disponible(cama):
            messages.error(request, "La cama seleccionada no está disponible.")
            return redirect("hospitalizacion:asignar_cama", paciente_id=paciente.id)

        # Crear asignación
        AsignacionCama.objects.create(paciente=paciente, cama=cama)

        # Cambiar estado de la cama
        cama.estado = "OCUPADA"
        cama.save()

        # 🔹 Crear cargo por cama asignada
        Cargo.objects.create(
            paciente=paciente,
            descripcion=f"Asignación de cama {cama.numero}",
            cantidad=1,
            precio_unitario=0,  # <-- aquí puedes poner un precio real si lo tienes
            cama=cama,
        )

        messages.success(request, "Cama asignada correctamente y cargo generado.")
        return redirect("paciente:detalle_paciente", paciente_id=paciente.id)

    return render(
        request,
        "hospitalizacion/asignar_cama.html",
        {
            "paciente": paciente,
            "camas": camas,
        },
    )


def liberar_cama(request, asignacion_id):
    asignacion = get_object_or_404(AsignacionCama, id=asignacion_id)

    if request.method == "POST":
        if asignacion.fecha_salida:
            messages.error(request, "Esta cama ya fue liberada.")
            return redirect(
                "paciente:detalle_paciente", paciente_id=asignacion.paciente.id
            )

        asignacion.fecha_salida = timezone.now()
        asignacion.save()

        cama = asignacion.cama
        cama.estado = "DISPONIBLE"
        cama.save()

        messages.success(request, "Cama liberada correctamente.")
        return redirect("paciente:detalle_paciente", paciente_id=asignacion.paciente.id)

    return render(
        request,
        "hospitalizacion/liberar_cama.html",
        {
            "asignacion": asignacion,
        },
    )


def trasladar_cama(request, asignacion_id):
    asignacion = get_object_or_404(AsignacionCama, id=asignacion_id)
    paciente = asignacion.paciente
    camas_disponibles = Cama.objects.filter(estado="DISPONIBLE").exclude(
        id=asignacion.cama.id
    )

    if request.method == "POST":
        nueva_cama_id = request.POST.get("nueva_cama_id")
        nueva_cama = get_object_or_404(Cama, id=nueva_cama_id)

        if not cama_disponible(nueva_cama):
            messages.error(request, "La nueva cama no está disponible.")
            return redirect(
                "hospitalizacion:trasladar_cama", asignacion_id=asignacion.id
            )

        asignacion.fecha_salida = timezone.now()
        asignacion.save()
        cama_actual = asignacion.cama
        cama_actual.estado = "DISPONIBLE"
        cama_actual.save()

        AsignacionCama.objects.create(paciente=paciente, cama=nueva_cama)
        nueva_cama.estado = "OCUPADA"
        nueva_cama.save()

        messages.success(request, "Paciente trasladado correctamente.")
        return redirect("paciente:detalle_paciente", paciente_id=paciente.id)

    return render(
        request,
        "hospitalizacion/trasladar_cama.html",
        {
            "asignacion": asignacion,
            "paciente": paciente,
            "camas_disponibles": camas_disponibles,
        },
    )


def historial_asignaciones(request):
    asignaciones = AsignacionCama.objects.select_related(
        "paciente", "cama", "cama__habitacion", "cama__habitacion__area"
    )
    return render(
        request,
        "hospitalizacion/historial_asignaciones.html",
        {
            "asignaciones": asignaciones,
        },
    )


"""def asignar_cama(request, id):
    asignacion = get_object_or_404(AsignacionCama, pk=id)

    Cargo.objects.create(
        paciente=asignacion.paciente,
        descripcion=f"Cama {asignacion.cama.numero}",
        cantidad=1,
        precio_unitario=asignacion.cama.precio,  # si tienes precio
        cama=asignacion.cama,
    )"""
