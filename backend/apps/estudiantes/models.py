from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Carrera(models.Model):
    """Modelo para representar una carrera académica"""
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre de la carrera')
    fija = models.BooleanField(default=False, verbose_name='Carrera fija del sistema', 
                              help_text='Si está marcada, esta carrera no puede ser modificada ni eliminada')
    activa = models.BooleanField(default=True, verbose_name='Activa')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    
    class Meta:
        verbose_name = 'Carrera'
        verbose_name_plural = 'Carreras'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def delete(self, *args, **kwargs):
        """Prevenir eliminación de carreras fijas"""
        if self.fija:
            raise ValidationError('No se puede eliminar una carrera fija del sistema.')
        super().delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        """Prevenir modificación de carreras fijas"""
        if self.pk:  # Si es una actualización
            try:
                old_instance = Carrera.objects.get(pk=self.pk)
                if old_instance.fija:
                    # Solo permitir cambios en el campo 'activa' para carreras fijas
                    if self.nombre != old_instance.nombre:
                        raise ValidationError('No se puede modificar el nombre de una carrera fija del sistema.')
            except Carrera.DoesNotExist:
                pass
        super().save(*args, **kwargs)


class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='estudiante')
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código de estudiante')
    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT, related_name='estudiantes', 
                                verbose_name='Carrera')
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
