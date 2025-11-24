from django.db import models


class TipoAlerta(models.TextChoices):
    """Tipos de alertas disponibles"""
    INFO = 'info', 'Información'
    WARNING = 'warning', 'Advertencia'
    DANGER = 'danger', 'Peligro'
    SUCCESS = 'success', 'Éxito'


class Alerta(models.Model):
    """Modelo para representar una alerta"""
    estudiante = models.ForeignKey('estudiantes.Estudiante', on_delete=models.CASCADE, related_name='alertas')
    tipo = models.CharField(max_length=20, choices=TipoAlerta.choices, default=TipoAlerta.INFO, verbose_name='Tipo')
    titulo = models.CharField(max_length=200, verbose_name='Título')
    mensaje = models.TextField(verbose_name='Mensaje')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_vencimiento = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de vencimiento')
    activa = models.BooleanField(default=True, verbose_name='Activa')
    leida = models.BooleanField(default=False, verbose_name='Leída')
    
    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.estudiante.codigo} - {self.titulo} ({self.tipo})"

