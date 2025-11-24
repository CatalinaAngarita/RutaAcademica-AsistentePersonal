from rest_framework import serializers
from .models import Materia


class MateriaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Materia"""
    prerequisitos_nombres = serializers.SerializerMethodField()
    
    class Meta:
        model = Materia
        fields = ['id', 'codigo', 'nombre', 'creditos', 'descripcion', 
                  'prerequisitos', 'prerequisitos_nombres', 'activa']
    
    def get_prerequisitos_nombres(self, obj):
        """Retorna los nombres de los prerequisitos"""
        return [{'id': p.id, 'codigo': p.codigo, 'nombre': p.nombre} 
                for p in obj.prerequisitos.all()]


class MateriaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar materias"""
    class Meta:
        model = Materia
        fields = ['id', 'codigo', 'nombre', 'creditos', 'activa']

