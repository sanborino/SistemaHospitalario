from rest_framework import serializers
from laboratorio.models import SolicitudLaboratorio, SolicitudDetalle


class SolicitudDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudDetalle
        fields = ["id", "estudio"]


class SolicitudLaboratorioSerializer(serializers.ModelSerializer):
    paciente = serializers.StringRelatedField()
    medico = serializers.StringRelatedField()
    detalles = SolicitudDetalleSerializer(source="solicituddetalle_set", many=True)

    class Meta:
        model = SolicitudLaboratorio
        fields = ["id", "paciente", "medico", "fecha", "estado", "detalles"]
