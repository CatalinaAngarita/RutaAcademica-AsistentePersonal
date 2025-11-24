from django.db import models


class Asistencia(models.Model):
    """Modelo para representar una asistencia"""
    estudiante = models.ForeignKey('estudiantes.Estudiante', on_delete=models.CASCADE, related_name='asistencias')
    materia = models.ForeignKey('materias.Materia', on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField(verbose_name='Fecha')
    asistio = models.BooleanField(default=True, verbose_name='Asistió')
    justificada = models.BooleanField(default=False, verbose_name='Justificada')
    observaciones = models.TextField(blank=True, null=True, verbose_name='Observaciones')
    
    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['-fecha', 'materia']
        unique_together = ['estudiante', 'materia', 'fecha']
    
    def __str__(self):
        estado = "Presente" if self.asistio else "Ausente"
        return f"{self.estudiante.codigo} - {self.materia.codigo} ({self.fecha}): {estado}"

