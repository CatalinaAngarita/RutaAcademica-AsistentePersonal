from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Sum
from .models import Nota
from .serializers import NotaSerializer, NotaCreateSerializer


class NotaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar notas"""
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NotaCreateSerializer
        return NotaSerializer
    
    def get_queryset(self):
        """Filtrar notas por estudiante si se proporciona"""
        queryset = Nota.objects.all()
        estudiante_id = self.request.query_params.get('estudiante', None)
        materia_id = self.request.query_params.get('materia', None)
        
        if estudiante_id:
            queryset = queryset.filter(estudiante_id=estudiante_id)
        if materia_id:
            queryset = queryset.filter(materia_id=materia_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def promedio_estudiante(self, request):
        """Obtener promedio de un estudiante"""
        estudiante_id = request.query_params.get('estudiante', None)
        if not estudiante_id:
            return Response({'error': 'Se requiere el parámetro estudiante'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        notas = Nota.objects.filter(estudiante_id=estudiante_id)
        
        if not notas.exists():
            return Response({
                'estudiante_id': estudiante_id,
                'promedio': 0,
                'total_notas': 0
            })
        
        suma_ponderada = sum(nota.valor_ponderado for nota in notas)
        total_porcentaje = sum(nota.porcentaje for nota in notas)
        
        promedio = 0
        if total_porcentaje > 0:
            promedio = (suma_ponderada / total_porcentaje) * 100
        
        return Response({
            'estudiante_id': estudiante_id,
            'promedio': round(promedio, 2),
            'total_notas': notas.count()
        })
    
    @action(detail=False, methods=['get'])
    def promedio_materia(self, request):
        """Obtener promedio de una materia"""
        materia_id = request.query_params.get('materia', None)
        if not materia_id:
            return Response({'error': 'Se requiere el parámetro materia'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        notas = Nota.objects.filter(materia_id=materia_id)
        
        if not notas.exists():
            return Response({
                'materia_id': materia_id,
                'promedio': 0,
                'total_notas': 0
            })
        
        suma_ponderada = sum(nota.valor_ponderado for nota in notas)
        total_porcentaje = sum(nota.porcentaje for nota in notas)
        
        promedio = 0
        if total_porcentaje > 0:
            promedio = (suma_ponderada / total_porcentaje) * 100
        
        return Response({
            'materia_id': materia_id,
            'promedio': round(promedio, 2),
            'total_notas': notas.count()
        })

