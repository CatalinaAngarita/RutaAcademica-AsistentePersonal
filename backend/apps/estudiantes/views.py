from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Estudiante, Carrera
from .serializers import EstudianteSerializer, EstudianteCreateSerializer, UserSerializer, CarreraSerializer


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


class CarreraViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para listar y consultar carreras (solo lectura)"""
    queryset = Carrera.objects.filter(activa=True).order_by('nombre')
    serializer_class = CarreraSerializer
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación
    
    def get_queryset(self):
        """Filtrar solo carreras activas"""
        queryset = Carrera.objects.filter(activa=True).order_by('nombre')
        return queryset


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Endpoint para iniciar sesión"""
    # Django REST Framework maneja CSRF automáticamente, pero podemos deshabilitarlo
    # para peticiones de API con autenticación por tokens
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Usuario y contraseña son requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if not user:
        return Response(
            {'error': 'Credenciales inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Verificar si el usuario tiene un perfil de estudiante
    try:
        estudiante = user.estudiante
    except Estudiante.DoesNotExist:
        return Response(
            {'error': 'El usuario no tiene un perfil de estudiante'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Obtener o crear token
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': UserSerializer(user).data,
        'estudiante': EstudianteSerializer(estudiante).data
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def registro_view(request):
    """Endpoint para registrar un nuevo estudiante"""
    try:
        serializer = EstudianteCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            estudiante = serializer.save()
            user = estudiante.user
            
            # Crear token para el nuevo usuario
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data,
                'estudiante': EstudianteSerializer(estudiante).data,
                'message': 'Estudiante registrado exitosamente'
            }, status=status.HTTP_201_CREATED)
        
        # Formatear errores para que sean más legibles
        errors = {}
        for field, error_list in serializer.errors.items():
            if isinstance(error_list, list):
                errors[field] = error_list[0] if error_list else 'Error de validación'
            else:
                errors[field] = str(error_list)
        
        return Response({
            'error': 'Error de validación',
            'errors': errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        import traceback
        print(f"Error en registro_view: {str(e)}")
        print(traceback.format_exc())
        return Response(
            {'error': f'Error interno del servidor: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_view(request):
    """Endpoint para obtener el perfil del estudiante autenticado"""
    try:
        estudiante = request.user.estudiante
        return Response({
            'user': UserSerializer(request.user).data,
            'estudiante': EstudianteSerializer(estudiante).data
        })
    except Estudiante.DoesNotExist:
        return Response(
            {'error': 'El usuario no tiene un perfil de estudiante'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Endpoint para cerrar sesión"""
    try:
        request.user.auth_token.delete()
    except:
        pass
    
    return Response({'message': 'Sesión cerrada exitosamente'})

