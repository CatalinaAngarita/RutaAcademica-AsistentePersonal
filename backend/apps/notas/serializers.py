from rest_framework import serializers
from .models import Nota
from apps.estudiantes.serializers import EstudianteSerializer
from apps.materias.serializers import MateriaListSerializer


class NotaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Nota"""
    estudiante = EstudianteSerializer(read_only=True)
    materia = MateriaListSerializer(read_only=True)
    valor_ponderado = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    
    class Meta:
        model = Nota
        fields = ['id', 'estudiante', 'materia', 'valor', 'porcentaje', 
                  'descripcion', 'fecha', 'valor_ponderado']
        read_only_fields = ['fecha']


class NotaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear una nota"""
    class Meta:
        model = Nota
        fields = ['estudiante', 'materia', 'valor', 'porcentaje', 'descripcion']
    
    def validate_valor(self, value):
        """Validar que el valor esté entre 0 y 20"""
        if value < 0 or value > 20:
            raise serializers.ValidationError("El valor debe estar entre 0 y 20")
        return value
    
    def validate_porcentaje(self, value):
        """Validar que el porcentaje esté entre 0 y 100"""
        if value < 0 or value > 100:
            raise serializers.ValidationError("El porcentaje debe estar entre 0 y 100")
        return value

