from django.db import models


class Nota(models.Model):
    """Modelo para representar una nota"""
    estudiante = models.ForeignKey('estudiantes.Estudiante', on_delete=models.CASCADE, related_name='notas')
    materia = models.ForeignKey('materias.Materia', on_delete=models.CASCADE, related_name='notas')
    valor = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Valor')
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Porcentaje')
    descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name='Descripción')
    fecha = models.DateField(auto_now_add=True, verbose_name='Fecha')
    
    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['-fecha', 'materia']
        unique_together = ['estudiante', 'materia', 'descripcion']
    
    def __str__(self):
        return f"{self.estudiante.codigo} - {self.materia.codigo}: {self.valor} ({self.porcentaje}%)"
    
    @property
    def valor_ponderado(self):
        """Calcula el valor ponderado de la nota"""
        return (self.valor * self.porcentaje) / 100

