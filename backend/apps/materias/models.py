from django.db import models


class Materia(models.Model):
    """Modelo para representar una materia"""
    codigo = models.CharField(max_length=20, unique=True, verbose_name='Código')
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    creditos = models.IntegerField(verbose_name='Créditos')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    prerequisitos = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='materias_requieren',
        verbose_name='Prerequisitos'
    )
    activa = models.BooleanField(default=True, verbose_name='Activa')
    
    class Meta:
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def puede_cursar(self, materias_aprobadas):
        """Verifica si la materia puede ser cursada basándose en prerequisitos"""
        prerequisitos = self.prerequisitos.all()
        if not prerequisitos.exists():
            return True
        return all(prereq in materias_aprobadas for prereq in prerequisitos)

