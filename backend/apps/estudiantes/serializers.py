from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Estudiante


class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class EstudianteSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Estudiante"""
    user = UserSerializer(read_only=True)
    nombre_completo = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    
    class Meta:
        model = Estudiante
        fields = ['id', 'user', 'codigo', 'carrera', 'semestre_actual', 
                  'fecha_ingreso', 'activo', 'nombre_completo', 'email']
        read_only_fields = ['fecha_ingreso']


class EstudianteCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear un estudiante con usuario"""
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Estudiante
        fields = ['codigo', 'carrera', 'semestre_actual', 'username', 
                  'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', ''),
        }
        
        user = User.objects.create_user(**user_data)
        estudiante = Estudiante.objects.create(user=user, **validated_data)
        return estudiante

