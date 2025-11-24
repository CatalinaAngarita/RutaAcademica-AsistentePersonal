from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Materia
from .serializers import MateriaSerializer, MateriaListSerializer
from .utils import construir_grafo_malla, obtener_ruta_academica


class MateriaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar materias"""
    queryset = Materia.objects.filter(activa=True)
    serializer_class = MateriaSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MateriaListSerializer
        return MateriaSerializer
    
    @action(detail=True, methods=['get'])
    def prerequisitos(self, request, pk=None):
        """Obtener prerequisitos de una materia"""
        materia = self.get_object()
        prerequisitos = materia.prerequisitos.all()
        serializer = MateriaListSerializer(prerequisitos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def malla_curricular(self, request):
        """Obtener la malla curricular como grafo"""
        materias = Materia.objects.filter(activa=True)
        grafo = construir_grafo_malla(materias)
        
        # Convertir grafo a formato JSON
        nodos = [{'id': m.id, 'codigo': m.codigo, 'nombre': m.nombre, 
                 'creditos': m.creditos} for m in materias]
        aristas = [{'source': edge[0], 'target': edge[1]} 
                  for edge in grafo.edges()]
        
        return Response({
            'nodos': nodos,
            'aristas': aristas
        })
    
    @action(detail=False, methods=['post'])
    def verificar_prerequisitos(self, request):
        """Verificar si un estudiante puede cursar ciertas materias"""
        materia_ids = request.data.get('materias', [])
        materias_aprobadas_ids = request.data.get('materias_aprobadas', [])
        
        materias = Materia.objects.filter(id__in=materia_ids)
        materias_aprobadas = Materia.objects.filter(id__in=materias_aprobadas_ids)
        
        resultado = []
        for materia in materias:
            puede_cursar = materia.puede_cursar(materias_aprobadas)
            prerequisitos_faltantes = []
            if not puede_cursar:
                prerequisitos = materia.prerequisitos.all()
                prerequisitos_faltantes = [
                    {'id': p.id, 'codigo': p.codigo, 'nombre': p.nombre}
                    for p in prerequisitos if p not in materias_aprobadas
                ]
            
            resultado.append({
                'materia': {
                    'id': materia.id,
                    'codigo': materia.codigo,
                    'nombre': materia.nombre
                },
                'puede_cursar': puede_cursar,
                'prerequisitos_faltantes': prerequisitos_faltantes
            })
        
        return Response(resultado)

