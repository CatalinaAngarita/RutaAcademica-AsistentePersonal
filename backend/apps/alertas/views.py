from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import models
from .models import Alerta, TipoAlerta
from .serializers import AlertaSerializer, AlertaCreateSerializer
from .utils import generar_alertas_automaticas


class AlertaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar alertas"""
    queryset = Alerta.objects.all()
    serializer_class = AlertaSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AlertaCreateSerializer
        return AlertaSerializer
    
    def get_queryset(self):
        """Filtrar alertas por estudiante y estado"""
        queryset = Alerta.objects.all()
        estudiante_id = self.request.query_params.get('estudiante', None)
        activa = self.request.query_params.get('activa', None)
        leida = self.request.query_params.get('leida', None)
        
        if estudiante_id:
            queryset = queryset.filter(estudiante_id=estudiante_id)
        if activa is not None:
            queryset = queryset.filter(activa=activa.lower() == 'true')
        if leida is not None:
            queryset = queryset.filter(leida=leida.lower() == 'true')
        
        # Filtrar alertas vencidas
        queryset = queryset.filter(
            models.Q(fecha_vencimiento__isnull=True) | 
            models.Q(fecha_vencimiento__gte=timezone.now())
        )
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        """Marcar una alerta como leída"""
        alerta = self.get_object()
        alerta.leida = True
        alerta.save()
        return Response(AlertaSerializer(alerta).data)
    
    @action(detail=False, methods=['post'])
    def generar_automaticas(self, request):
        """Generar alertas automáticas para un estudiante"""
        estudiante_id = request.data.get('estudiante', None)
        if not estudiante_id:
            return Response({'error': 'Se requiere el parámetro estudiante'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        from apps.estudiantes.models import Estudiante
        try:
            estudiante = Estudiante.objects.get(id=estudiante_id)
        except Estudiante.DoesNotExist:
            return Response({'error': 'Estudiante no encontrado'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        alertas_generadas = generar_alertas_automaticas(estudiante)
        
        return Response({
            'estudiante_id': estudiante_id,
            'alertas_generadas': len(alertas_generadas),
            'alertas': AlertaSerializer(alertas_generadas, many=True).data
        })

