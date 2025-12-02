from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EstudianteViewSet, 
    CarreraViewSet,
    login_view,
    registro_view,
    perfil_view,
    logout_view
)

router = DefaultRouter()
router.register(r'estudiantes', EstudianteViewSet, basename='estudiante')
router.register(r'carreras', CarreraViewSet, basename='carrera')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', login_view, name='login'),
    path('auth/registro/', registro_view, name='registro'),
    path('auth/perfil/', perfil_view, name='perfil'),
    path('auth/logout/', logout_view, name='logout'),
]

