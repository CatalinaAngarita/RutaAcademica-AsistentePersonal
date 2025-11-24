"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.estudiantes.urls')),
    path('api/', include('apps.materias.urls')),
    path('api/', include('apps.notas.urls')),
    path('api/', include('apps.asistencias.urls')),
    path('api/', include('apps.alertas.urls')),
    path('', index, name='index'),
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    # Servir CSS y JS directamente desde frontend
    from django.views.static import serve
    from django.urls import re_path
    frontend_dir = settings.BASE_DIR.parent / 'frontend'
    urlpatterns += [
        re_path(r'^css/(?P<path>.*)$', serve, {'document_root': frontend_dir / 'css'}),
        re_path(r'^js/(?P<path>.*)$', serve, {'document_root': frontend_dir / 'js'}),
    ]
