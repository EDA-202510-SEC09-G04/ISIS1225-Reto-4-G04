from DataStructures.Graph import digraph as gr
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Priority_queue import priority_queue as pq


def dijkstra(graph, start_node):
    """Dijkstra adaptado a tu estructura de grafo"""
    if not gr.contains_vertex(graph, start_node):
        raise ValueError("Nodo inicial no existe")
    
    # Inicialización
    distances = {node: float('inf') for node in gr.vertices(graph)}
    distances[start_node] = 0
    previous = {node: None for node in gr.vertices(graph)}
    
    pqueue = pq.newPriorityQueue()
    pq.enqueue(pqueue, start_node, 0)
    
    while not pq.isEmpty(pqueue):
        current = pq.dequeue(pqueue)
        
        # Obtener aristas del nodo actual
        edges = gr.edges_vertex(graph, current)
        for _, neighbor, weight in edges:
            alt = distances[current] + weight
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                previous[neighbor] = current
                pq.enqueue(pqueue, neighbor, alt)
    
    return distances, previous


def shortest_path(graph, start, end):
    """Obtiene el camino más corto entre dos nodos"""
    distances, previous = dijkstra(graph, start)
    path = []
    current = end
    
    if previous[current] is None and current != start:
        return None  # No hay camino
    
    while current is not None:
        path.insert(0, current)
        current = previous[current]
    
    return {
        'path': path,
        'distance': distances[end],
        'nodes_visited': len([d for d in distances.values() if d != float('inf')])
    }