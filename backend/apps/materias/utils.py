import networkx as nx
from .models import Materia


def construir_grafo_malla(materias):
    """
    Construye un grafo dirigido de la malla curricular usando networkx
    
    Args:
        materias: QuerySet de materias
    
    Returns:
        networkx.DiGraph: Grafo dirigido de la malla curricular
    """
    G = nx.DiGraph()
    
    # Agregar nodos (materias)
    for materia in materias:
        G.add_node(materia.id, 
                   codigo=materia.codigo,
                   nombre=materia.nombre,
                   creditos=materia.creditos)
    
    # Agregar aristas (prerequisitos)
    for materia in materias:
        for prerequisito in materia.prerequisitos.all():
            if prerequisito.id in G.nodes():
                G.add_edge(prerequisito.id, materia.id)
    
    return G


def obtener_ruta_academica(materias_aprobadas, materias_objetivo):
    """
    Obtiene la ruta académica recomendada para cursar ciertas materias
    
    Args:
        materias_aprobadas: Lista de IDs de materias aprobadas
        materias_objetivo: Lista de IDs de materias objetivo
    
    Returns:
        dict: Ruta académica con orden sugerido
    """
    todas_materias = Materia.objects.filter(activa=True)
    grafo = construir_grafo_malla(todas_materias)
    
    # Orden topológico para determinar el orden de cursado
    try:
        orden_topologico = list(nx.topological_sort(grafo))
    except nx.NetworkXError:
        # Si hay ciclos, usar orden por código
        orden_topologico = sorted([m.id for m in todas_materias])
    
    # Filtrar materias que pueden ser cursadas
    materias_disponibles = []
    materias_aprobadas_set = set(materias_aprobadas)
    
    for materia_id in orden_topologico:
        if materia_id in materias_aprobadas_set:
            continue
        
        materia = Materia.objects.get(id=materia_id)
        if materia.puede_cursar([Materia.objects.get(id=mid) for mid in materias_aprobadas_set]):
            materias_disponibles.append(materia)
    
    return {
        'orden_sugerido': [{'id': m.id, 'codigo': m.codigo, 'nombre': m.nombre} 
                          for m in materias_disponibles],
        'total_materias': len(materias_disponibles)
    }

