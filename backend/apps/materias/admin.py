from django.contrib import admin
from .models import Materia


@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'creditos', 'activa']
    list_filter = ['activa', 'creditos']
    search_fields = ['codigo', 'nombre']
    filter_horizontal = ['prerequisitos']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'creditos', 'descripcion', 'activa')
        }),
        ('Prerequisitos', {
            'fields': ('prerequisitos',)
        }),
    )

