from DataStructures.Queue import queue as qu
from DataStructures.Graph import digraph as gr


def bfs(graph, start_node):
    if not gr.contains_vertex(graph, start_node):
        raise ValueError("Nodo inicial no existe")
    
    visited = set()
    order = []
    queue = qu.newQueue()
    qu.enqueue(queue, start_node)
    
    while not qu.isEmpty(queue):
        current = qu.dequeue(queue)
        if current not in visited:
            visited.add(current)
            order.append(current)
            
            # Obtener vecinos
            adj_nodes = gr.adjacents(graph, current)
            for neighbor in adj_nodes:
                if neighbor not in visited:
                    qu.enqueue(queue, neighbor)
    
    return order