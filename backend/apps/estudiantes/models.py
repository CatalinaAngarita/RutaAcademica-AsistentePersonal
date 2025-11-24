from django.db import models
from django.contrib.auth.models import User


class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='estudiante')
    codigo = models.CharField(max_length=20, unique=True, verbose_name='CÃ³digo de estudiante')
    carrera = models.CharField(max_length=100, verbose_name='Carrera')
    semestre_actual = models.IntegerField(default=1, verbose_name='Semestre actual')
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name='Fecha de ingreso')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    
    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.user.get_full_name() or self.user.username}"
    
    @property
    def nombre_completo(self):
        return self.user.get_full_name() or self.user.username
    
    @property
    def email(self):
        return self.user.email
