from rest_framework import serializers
from .models import Alerta, TipoAlerta
from apps.estudiantes.serializers import EstudianteSerializer


class AlertaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Alerta"""
    estudiante = EstudianteSerializer(read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Alerta
        fields = ['id', 'estudiante', 'tipo', 'tipo_display', 'titulo', 'mensaje',
                  'fecha_creacion', 'fecha_vencimiento', 'activa', 'leida']
        read_only_fields = ['fecha_creacion']


class AlertaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear una alerta"""
    class Meta:
        model = Alerta
        fields = ['estudiante', 'tipo', 'titulo', 'mensaje', 'fecha_vencimiento', 'activa']

