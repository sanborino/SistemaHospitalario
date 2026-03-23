from .models import AsignacionCama


def cama_disponible(cama):
    return cama.estado == "DISPONIBLE"


def paciente_con_cama_activa(paciente):
    return AsignacionCama.objects.filter(
        paciente=paciente, fecha_salida__isnull=True
    ).exists()
