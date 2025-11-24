from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Asistencia
from .serializers import AsistenciaSerializer, AsistenciaCreateSerializer


class AsistenciaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar asistencias"""
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AsistenciaCreateSerializer
        return AsistenciaSerializer
    
    def get_queryset(self):
        """Filtrar asistencias por estudiante o materia si se proporciona"""
        queryset = Asistencia.objects.all()
        estudiante_id = self.request.query_params.get('estudiante', None)
        materia_id = self.request.query_params.get('materia', None)
        
        if estudiante_id:
            queryset = queryset.filter(estudiante_id=estudiante_id)
        if materia_id:
            queryset = queryset.filter(materia_id=materia_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def estadisticas_estudiante(self, request):
        """Obtener estadísticas de asistencia de un estudiante"""
        estudiante_id = request.query_params.get('estudiante', None)
        if not estudiante_id:
            return Response({'error': 'Se requiere el parámetro estudiante'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        asistencias = Asistencia.objects.filter(estudiante_id=estudiante_id)
        
        if not asistencias.exists():
            return Response({
                'estudiante_id': estudiante_id,
                'porcentaje_asistencia': 0,
                'total_clases': 0,
                'presentes': 0,
                'ausentes': 0
            })
        
        total = asistencias.count()
        presentes = asistencias.filter(asistio=True).count()
        ausentes = total - presentes
        porcentaje = (presentes / total) * 100
        
        return Response({
            'estudiante_id': estudiante_id,
            'porcentaje_asistencia': round(porcentaje, 2),
            'total_clases': total,
            'presentes': presentes,
            'ausentes': ausentes
        })
    
    @action(detail=False, methods=['get'])
    def estadisticas_materia(self, request):
        """Obtener estadísticas de asistencia de una materia"""
        materia_id = request.query_params.get('materia', None)
        if not materia_id:
            return Response({'error': 'Se requiere el parámetro materia'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        asistencias = Asistencia.objects.filter(materia_id=materia_id)
        
        if not asistencias.exists():
            return Response({
                'materia_id': materia_id,
                'porcentaje_asistencia': 0,
                'total_clases': 0,
                'presentes': 0,
                'ausentes': 0
            })
        
        total = asistencias.count()
        presentes = asistencias.filter(asistio=True).count()
        ausentes = total - presentes
        porcentaje = (presentes / total) * 100
        
        return Response({
            'materia_id': materia_id,
            'porcentaje_asistencia': round(porcentaje, 2),
            'total_clases': total,
            'presentes': presentes,
            'ausentes': ausentes
        })

