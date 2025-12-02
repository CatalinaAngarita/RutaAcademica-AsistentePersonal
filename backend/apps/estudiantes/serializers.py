from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Estudiante, Carrera


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CarreraSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Carrera"""
    class Meta:
        model = Carrera
        fields = ['id', 'nombre', 'fija', 'activa']


class EstudianteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Estudiante"""
    user = UserSerializer(read_only=True)
    carrera = CarreraSerializer(read_only=True)
    carrera_id = serializers.PrimaryKeyRelatedField(
        queryset=Carrera.objects.filter(activa=True),
        source='carrera',
        write_only=True,
        required=False
    )
    nombre_completo = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    
    class Meta:
        model = Estudiante
        fields = ['id', 'user', 'codigo', 'carrera', 'carrera_id', 'semestre_actual', 
                  'fecha_ingreso', 'activo', 'nombre_completo', 'email']
        read_only_fields = ['fecha_ingreso']


class EstudianteCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear un estudiante con usuario"""
    username = serializers.CharField(write_only=True, min_length=3, max_length=150)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, min_length=3)
    first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    codigo = serializers.CharField(max_length=20, min_length=1)
    carrera_id = serializers.PrimaryKeyRelatedField(
        queryset=Carrera.objects.filter(activa=True),
        source='carrera',
        write_only=True
    )
    semestre_actual = serializers.IntegerField(min_value=1, max_value=20, default=1)
    
    class Meta:
        model = Estudiante
        fields = ['codigo', 'carrera_id', 'semestre_actual', 'username', 
                  'email', 'password', 'first_name', 'last_name']
    
    def validate_codigo(self, value):
        """Validar que el código no exista ya"""
        if Estudiante.objects.filter(codigo=value).exists():
            raise serializers.ValidationError('Este código de estudiante ya está registrado.')
        return value
    
    def validate_username(self, value):
        """Validar que el username no exista ya"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Este nombre de usuario ya está en uso.')
        return value
    
    def validate_email(self, value):
        """Validar que el email no exista ya"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Este correo electrónico ya está registrado.')
        return value
    
    def create(self, validated_data):
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', ''),
        }
        
        try:
            user = User.objects.create_user(**user_data)
            estudiante = Estudiante.objects.create(user=user, **validated_data)
            return estudiante
        except Exception as e:
            # Si hay error al crear, eliminar el usuario si se creó
            if 'user' in locals():
                user.delete()
            raise serializers.ValidationError(f'Error al crear el estudiante: {str(e)}')

