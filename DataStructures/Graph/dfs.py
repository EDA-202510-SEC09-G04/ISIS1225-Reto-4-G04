from DataStructures.Graph import digraph as gr
from DataStructures.Stack import stack as st

def dfs(graph, start_node):
    """DFS adaptado a tu estructura de grafo"""
    if not gr.contains_vertex(graph, start_node):
        raise ValueError("Nodo inicial no existe")
    
    visited = set()
    order = []
    stack = st.newStack()
    st.push(stack, start_node)
    
    while not st.isEmpty(stack):
        current = st.pop(stack)
        if current not in visited:
            visited.add(current)
            order.append(current)
            
            # Obtener vecinos
            adj_nodes = gr.adjacents(graph, current)
            for neighbor in adj_nodes:
                if neighbor not in visited:
                    st.push(stack, neighbor)
    
    return order