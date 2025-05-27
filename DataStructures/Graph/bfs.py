from DataStructures.Queue import queue as qu
from DataStructures.Graph import digraph as gr


def bfs(graph, start_node):
    if not gr.contains_vertex(graph, start_node):
        raise ValueError("Nodo inicial no existe")
    
    visited = set()
    parent = {}
    order = []
    queue = qu.new_queue()
    qu.enqueue(queue, start_node)
    
    
    while not qu.is_empty(queue):
        current = qu.dequeue(queue)
        if current not in visited:
            visited.add(current)
            order.append(current)
            
            # Obtener vecinos
            if current is not None:
              adj_nodes = gr.adjacents(graph, current)
               
            for neighbor in adj_nodes['elements']:
                    
                   if neighbor not in visited and neighbor not in parent and neighbor is not None:
                        parent[neighbor] = current
                        qu.enqueue(queue, neighbor)
    
    return {'order':order,'parent':parent}