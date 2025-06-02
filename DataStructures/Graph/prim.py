# In DataStructures/Graph/prim.py (or whatever your prim.py is called)

from DataStructures.Map import map_linear_probing as map
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Queue import queue as q
from DataStructures.Graph import digraph as g 
from DataStructures.Graph import edge as edg 
from DataStructures.List import array_list as lt


def new_prim_structure(my_graph, source): 


    structure = {
        'source': source,
        'edge_to': None,   # map: vertex_key -> edge_object (cheapest edge to vertex from MST)
        'dist_to': None,   # map: vertex_key -> float (min weight of such edge)
        'marked': None,    # map: vertex_key -> bool (is vertex in MST?)
        'pq': None,        # priority_queue: (dist_to[v], v) for unvisited vertices
        'mst_edges_queue': None # Queue to store the edges that form the MST
    } 
    

    order_capacity = g.order(my_graph) 

  
    structure['edge_to'] = map.new_map(order_capacity, 0.5)
    structure['dist_to'] = map.new_map(order_capacity, 0.5)
    structure['marked'] = map.new_map(order_capacity, 0.5)
    
    
    structure['pq'] = pq.new_heap(is_min_pq=True) 

   
    structure['mst_edges_queue'] = q.new_queue() # Using your queue.py

    return structure



def prim_mst(my_graph, source):
    """
    Implementa el algoritmo de Prim para encontrar el arbol de expansion minima
    de un grafo no dirigido y conexo. El algoritmo inicia en el vertice source
    y va agregando arcos de menor peso que conecten vertices que no esten en el
    arbol de expansion minima. El algoritmo termina cuando todos los vertices
    estan en el arbol de expansion minima.

    Parameters:
    my_graph (no_digraph) – El grafo a examinar (asumido no dirigido y conexo).
    source (any) – El vertice fuente.

    Returns:
    La estructura prim_search con los resultados del MST.
    """
    
    # 1. Validar que el vértice fuente existe en el grafo
    if g.get_vertex_info(my_graph, source) is None:
        raise ValueError(f"El vértice fuente '{source}' no se encuentra en el grafo.")

    # 2. Inicializar la estructura de búsqueda para Prim
    search_structure = new_prim_structure(my_graph, source)

    # 3. Obtener todos los vértices del grafo para inicializar distancias
    all_vertices_keys = g.vertices(my_graph)

    # 4. Inicializar distancias: infinito para todos los vértices, 0 para el origen
    #    e insertar en la cola de prioridad.
    for i in range(lt.size(all_vertices_keys)):
        v_key = lt.get_element(all_vertices_keys, i)
        map.put(search_structure['dist_to'], v_key, float('inf')) # Distancia inicial infinita
        map.put(search_structure['marked'], v_key, False)         # Ningún vértice marcado al inicio
        # edge_to se inicializa implícitamente a None por el mapa
    
    # 5. Establecer la distancia del vértice fuente a 0 y añadirlo a la cola de prioridad.
    #    (El item en la PQ es la clave del vértice, la prioridad es la distancia)
    map.put(search_structure['dist_to'], source, 0.0) 
    pq.put(search_structure['pq'], 0.0, source) # Prioridad 0, item 'source'

    #print(f"  PRIM DEBUG: Iniciando Prim desde el vértice '{source}'.")

    # 6. Bucle principal de Prim: Continúa mientras la PQ no esté vacía
    #    y el MST aún no contenga todos los vértices (implícito por marcado).
    while not pq.is_empty(search_structure['pq']):
        # Extraer el vértice con la distancia mínima a un vértice ya en el MST
        # del Min-Priority Queue. Retorna (prioridad, item_value) -> (distancia, vertice_actual)
        (min_dist, v_key) = pq.del_min(search_structure['pq'])

        # Si el vértice ya ha sido marcado (es decir, ya está en el MST), lo saltamos.
        # Esto ocurre con implementaciones 'perezosas' (lazy) de Prim.
        if map.get(search_structure['marked'], v_key):
            #print(f"  PRIM DEBUG: Vértice '{v_key}' ya está en el MST. Saltando.")
            continue
        
        # Marcar el vértice 'v_key' como parte del MST
        map.put(search_structure['marked'], v_key, True)
        
        #print(f"  PRIM DEBUG: Añadiendo vértice '{v_key}' al MST. Costo = {min_dist}.")

        # Si hay una arista asociada a este vértice (no es el origen), añadirla a la cola de aristas del MST
        if map.get(search_structure['edge_to'], v_key) is not None:
            mst_edge = map.get(search_structure['edge_to'], v_key)
            q.enqueue(search_structure['mst_edges_queue'], mst_edge)
            #print(f"  PRIM DEBUG: Añadida arista al MST: '{mst_edge['from']}'--'{mst_edge['to']}' (peso {mst_edge['weight']}).")


        # Relajar las aristas adyacentes a 'v_key'
        # Es decir, revisar si al añadir 'v_key' se pueden encontrar caminos más baratos
        # para conectar los vecinos no marcados al MST.
        
        # Obtener los adyacentes de 'v_key'
        adj_vertices_list = g.adjacents(my_graph, v_key) # Retorna array_list de claves de vecinos
        
        list_size_adj = lt.size(adj_vertices_list)
        for i in range(list_size_adj):
            w_key = lt.get_element(adj_vertices_list, i) # Un vecino de v_key
            
            # Solo consideramos vecinos que aún no están en el MST (no marcados)
            if not map.get(search_structure['marked'], w_key):
                # Obtener la arista entre v_key y w_key (y su peso)
                # En un grafo no dirigido, g.get_adjacents(my_graph, v_key) devuelve un mapa
                # que tiene el peso de la arista (v_key, w_key).
                edge_vw = map.get(g.get_adjacents(my_graph, v_key), w_key)
                edge_weight = edg.weight(edge_vw) # Asume edg.weight() funciona

                # Si encontramos un camino más barato a 'w_key' desde 'v_key'
                if edge_weight < map.get(search_structure['dist_to'], w_key):
                    # Actualizar la distancia mínima para 'w_key'
                    map.put(search_structure['dist_to'], w_key, edge_weight)
                    # Almacenar la arista que proporciona esta menor distancia
                    # Necesitamos la arista completa: ('from', 'to', 'weight')
                    # Ya que edg.new_edge crea {'to': key_v, 'weight': weight}
                    # Podríamos necesitar añadir un campo 'from' al edge o crear un dict temp.
                    # Para simplificar, crearemos un dict temporal con 'from', 'to', 'weight'.
                    # O incluso mejor, hacer que edg.new_edge acepte 'from' y 'to'.
                    # Asumamos que edg.new_edge(key_v, weight) es en realidad solo key_v=to.
                    # Para Prim, edge_to debe ser el vértice del que v_key vino.
                    # El 'edge_to' debe almacenar la arista completa, o al menos el vértice predecesor y el peso.
                    
                    # Vamos a modificar lo que edge_to guarda para Prim:
                    # 'edge_to[w_key]' guarda la arista que conecta 'w_key' al MST.
                    # Será { 'from': v_key, 'to': w_key, 'weight': edge_weight }
                    map.put(search_structure['edge_to'], w_key, {
                        'from': v_key, 
                        'to': w_key, 
                        'weight': edge_weight
                    })
                    
                    # Insertar/actualizar 'w_key' en la PQ con su nueva distancia mínima
                    # Esto es para la implementación 'perezosa' (lazy Prim)
                    pq.put(search_structure['pq'], edge_weight, w_key)
                    #print(f"    PRIM DEBUG: Relajando arista '{v_key}'--'{w_key}'. Nuevo dist_to[{w_key}]={edge_weight}. Añadido a PQ.")
                
                    #print(f"    PRIM DEBUG: Arista '{v_key}'--'{w_key}' (peso {edge_weight}) no mejora la distancia a '{w_key}'.")

    #print(f"  PRIM DEBUG: Algoritmo Prim finalizado. Total aristas MST en cola: {q.size(search_structure['mst_edges_queue'])}.")
    return search_structure


# In DataStructures/Graph/prim.py

# ... (prim_mst function goes here) ...

def edges_mst(my_graph, aux_structure):
    """
    Retorna los arcos del arbol de expansion minima (MST) en una cola.
    Precondición: Se debe haber ejecutado previamente la funcion prim_mst.

    Parameters:
    my_graph (no_digraph) – El grafo a examinar.
    aux_structure (prim_search) – La estructura de busqueda que contiene los resultados de Prim.

    Returns:
    La cola (queue) con los arcos del MST (cada arco como un diccionario {'from', 'to', 'weight'}).
    """
    # La cola de aristas ya está en la estructura de búsqueda.
    # Como q.new_queue() ahora devuelve directamente un array_list,
    # aux_structure['mst_edges_queue'] es el array_list en sí.
    return aux_structure['mst_edges_queue'] # Returns the array_list object directly


def weight_mst(my_graph, aux_structure):
    """
    Retorna el peso total del arbol de expansion minima (MST).
    Precondición: Se debe haber ejecutado previamente la funcion prim_mst.

    Parameters:
    my_graph (no_digraph) – El grafo a examinar.
    aux_structure (prim_search) – La estructura de busqueda que contiene los resultados de Prim.

    Returns:
    El peso total del arbol de expansion minima (float).
    """
    total_weight = 0.0
    
    # La cola de aristas del MST está en aux_structure['mst_edges_queue'].
    # Esta cola *es* el array_list.
    mst_edges_array_list = aux_structure['mst_edges_queue'] # <--- FIX: Use the queue object directly

    # Iterar sobre los elementos del array_list
    for i in range(lt.size(mst_edges_array_list)): # <--- FIX: Call lt.size() on the array_list object
        edge = lt.get_element(mst_edges_array_list, i) # <--- FIX: Call lt.get_element() on the array_list object
        total_weight += edge['weight'] # Sumar el peso de cada arista

    return total_weight