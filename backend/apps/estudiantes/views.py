from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Estudiante
from .serializers import EstudianteSerializer, EstudianteCreateSerializer, UserSerializer


class EstudianteViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar estudiantes"""
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EstudianteCreateSerializer
        return EstudianteSerializer
    
    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Obtener estadísticas del estudiante"""
        estudiante = self.get_object()
        
        # Importar aquí para evitar importaciones circulares
        from apps.notas.models import Nota
        from apps.asistencias.models import Asistencia
        
        notas = Nota.objects.filter(estudiante=estudiante)
        asistencias = Asistencia.objects.filter(estudiante=estudiante)
        
        # Calcular promedio general
        promedio = 0
        if notas.exists():
            suma_ponderada = sum(nota.valor * (nota.porcentaje / 100) for nota in notas)
            total_porcentaje = sum(nota.porcentaje for nota in notas)
            if total_porcentaje > 0:
                promedio = suma_ponderada / (total_porcentaje / 100)
        
        # Calcular asistencia promedio
        asistencia_promedio = 0
        if asistencias.exists():
            total = asistencias.count()
            presentes = asistencias.filter(asistio=True).count()
            asistencia_promedio = (presentes / total) * 100
        
        return Response({
            'estudiante': EstudianteSerializer(estudiante).data,
            'promedio_general': round(promedio, 2),
            'asistencia_promedio': round(asistencia_promedio, 2),
            'total_notas': notas.count(),
            'total_asistencias': asistencias.count(),
        })

