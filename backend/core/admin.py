"""
Configuración personalizada del Admin Site
"""
from django.contrib import admin

# Personalizar el admin site estándar (que unfold reemplaza automáticamente)
admin.site.site_header = "Ruta Académica - Administración"
admin.site.site_title = "Ruta Académica"
admin.site.index_title = "Panel de Administración"
