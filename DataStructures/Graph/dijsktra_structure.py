from DataStructures.Graph import digraph as G
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Priority_queue import priority_queue as pq


def new_dijsktra_structure(source, g_order):
    """

    Crea una estructura de busqueda usada en el algoritmo **dijsktra**.

    Se crea una estructura de busqueda con los siguientes atributos:

    - **source**: Vertice de origen. Se inicializa en ``source``
    - **visited**: Mapa con los vertices visitados. Se inicializa en ``None``
    - **pq**: Cola indexada con los vertices visitados. Se inicializa en ``None``

    :returns: Estructura de busqueda
    :rtype: dijsktra_search
    """
    structure = {
        "source": source,
        "visited": mp.new_map(
            g_order, 0.5),
        "pq": pq.new_heap()}
    return structure

def dijkstra(graph, source):
    order = G.num_vertices(graph)
    structure = new_dijsktra_structure(source, order)

    dist = {}
    prev = {}

    # Inicializar estructuras
    for vertex in G.vertices(graph):
        dist[vertex] = float('inf')
        prev[vertex] = None
        mp.put(structure["visited"], vertex, False)

    dist[source] = 0
    pq.insert(structure["pq"], source, 0)

    while not pq.is_empty(structure["pq"]):
        current = pq.del_min(structure["pq"])[0]  # devuelve (vertex, key)
        mp.put(structure["visited"], current, True)

        neighbors = G.adjacents(graph, current)
        while not lt.is_empty(neighbors):
            neighbor = lt.remove_first(neighbors)
            if not mp.get(structure["visited"], neighbor)['value']:
                weight = G.get_edge_weight(graph, current, neighbor)
                alt = dist[current] + weight
                if alt < dist[neighbor]:
                    dist[neighbor] = alt
                    prev[neighbor] = current
                    pq.insert(structure["pq"], neighbor, alt)

    return dist, prev
