"""
Configuración personalizada del Admin Site
"""
from django.contrib import admin

# Personalizar el admin site estándar (que unfold reemplaza automáticamente)
admin.site.site_header = "Ruta Académica - Administración"
admin.site.site_title = "Ruta Académica"
admin.site.index_title = "Panel de Administración"

# Guardar el método original
_original_get_app_list = admin.site.get_app_list

def custom_get_app_list(self, request):
    """
    Personaliza la lista para ELIMINAR la duplicación.
    Cuando una app tiene un solo modelo, oculta completamente el nombre de la app.
    """
    app_list = _original_get_app_list(self, request)
    
    # Procesar cada app en la lista
    processed_apps = []
    for app in app_list:
        app_label = app.get('app_label', '')
        models = app.get('models', [])
        app_name = app.get('name', '')
        
        # Si la app tiene un solo modelo
        if len(models) == 1:
            model = models[0]
            model_name = model.get('name', '')
            
            # Si el nombre de la app y el modelo son iguales o muy similares
            if (app_name.lower() == model_name.lower() or 
                app_name.lower().strip() == model_name.lower().strip()):
                # Crear una entrada que muestre SOLO el modelo como si fuera el nivel superior
                # Hacer que el nombre de la app sea igual al modelo para que unfold lo trate como uno solo
                app['name'] = model_name
                # Hacer que el modelo tenga el mismo nombre para evitar duplicación visual
                model['name'] = model_name
                # Mantener la estructura pero con nombres iguales para que unfold lo colapse
                processed_apps.append(app)
            else:
                processed_apps.append(app)
        else:
            # Si tiene múltiples modelos, mantener como está
            processed_apps.append(app)
    
    return processed_apps

# Reemplazar el método usando types.MethodType para que funcione correctamente
import types
admin.site.get_app_list = types.MethodType(custom_get_app_list, admin.site)
