from rest_framework import serializers
from .models import Asistencia
from apps.estudiantes.serializers import EstudianteSerializer
from apps.materias.serializers import MateriaListSerializer


class AsistenciaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Asistencia"""
    estudiante = EstudianteSerializer(read_only=True)
    materia = MateriaListSerializer(read_only=True)
    
    class Meta:
        model = Asistencia
        fields = ['id', 'estudiante', 'materia', 'fecha', 'asistio', 
                  'justificada', 'observaciones']


class AsistenciaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear una asistencia"""
    class Meta:
        model = Asistencia
        fields = ['estudiante', 'materia', 'fecha', 'asistio', 'justificada', 'observaciones']

