from DataStructures.Map import map_linear_probing as mp
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Queue import queue as q
from DataStructures.Graph import digraph as gr

def prim_domiciliario(graph, start_node, domiciliario_id):
    """Árbol de recubrimiento mínimo para rutas de un domiciliario"""
    if not gr.contains_vertex(graph, start_node):
        raise ValueError("Nodo inicial no existe")
    
    tree = []
    visited = set([start_node])
    edges = []
    
    # Filtrar aristas usadas por el domiciliario
    for u, v, w in all_edges_used_by(graph, domiciliario_id):
        edges.append((w, u, v))
    
    heap = pq.newPriorityQueue()
    for edge in edges:
        pq.enqueue(heap, edge, edge[0])
    
    while not pq.isEmpty(heap) and len(visited) < gr.order(graph):
        w, u, v = pq.dequeue(heap)
        if v not in visited:
            visited.add(v)
            tree.append((u, v, w))
            # Agregar nuevas aristas del nodo v
            for _, neighbor, weight in gr.edges_vertex(graph, v):
                if neighbor not in visited:
                    pq.enqueue(heap, (weight, v, neighbor), weight)
    
    return tree


def all_edges_used_by(graph, domiciliario_id):
    """Obtiene todas las aristas usadas por un domiciliario"""
    edges = []
    for node in gr.vertices(graph):
        node_info = gr.get_vertex_information(graph, node)
        if domiciliario_id in node_info['info']['domiciliarios']:
            edges.extend(gr.edges_vertex(graph, node))
    return edges