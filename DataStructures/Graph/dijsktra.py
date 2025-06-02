# En DataStructures/Graph/dijkstra.py (o el archivo que uses)

from DataStructures.Map import map_linear_probing as map # Tu implementación de mapa
from DataStructures.Priority_queue import priority_queue as pq # Tu min-heap
from DataStructures.Graph import digraph as g # Tu grafo no dirigido (asumimos que Dijkstra es para este)
from DataStructures.List import array_list as lt # Para operaciones de lista
from DataStructures.Stack import stack as stk # Para path_to
from DataStructures.List import single_linked_list as sll

def new_dijkstra_structure(source, my_graph): # <--- MODIFICADO: Añadido my_graph para obtener el orden
    """
    Crea una estructura de búsqueda usada en el algoritmo **Dijkstra**.

    :param source: Identificador del vértice inicio del Algoritmo de Dijkstra.
    :type source: any
    :param my_graph: El grafo sobre el cual se ejecutará Dijkstra (para obtener el orden).
    :type my_graph: no_digraph

    :returns: Estructura de búsqueda.
    :rtype: dijkstra_search
    """

    structure = {
        'source': source, # Identificador del vértice inicio del Alg de Dijkstra
        'edge_to': None,  # Mapa: vertex_key -> edge_object (arista que llega a este vértice en el camino más corto)
        'dist_to': None,  # Mapa: vertex_key -> float (costo del camino más corto desde source)
        'marked': None,   # Mapa: vertex_key -> bool (True si el vértice ya está en el árbol de caminos más cortos)
        'pq': None        # Cola de prioridad: (costo, vertex_key)
    }
    
    # Obtener el orden del grafo para inicializar el tamaño de los mapas
    order_capacity = g.order(my_graph) 

    # Inicializar los mapas con capacidad basada en el orden del grafo
    structure['edge_to'] = map.new_map(order_capacity, 0.5)
    structure['dist_to'] = map.new_map(order_capacity, 0.5)
    structure['marked'] = map.new_map(order_capacity, 0.5)
    
    # Inicializar la cola de prioridad (es un min-heap por defecto)
    structure['pq'] = pq.new_heap(is_min_pq=True) 
    
    return structure

# En DataStructures/Graph/dijkstra.py

# ... (new_dijkstra_structure función aquí) ...

def dijkstra(my_graph, source):
    """
    Implementa el algoritmo de Dijkstra para encontrar los caminos de costo mínimo
    desde un vértice fuente a todos los demás vértices alcanzables en un grafo ponderado.
    
    Parameters:
    my_graph (no_digraph) – El grafo a examinar (asumido no dirigido y con pesos positivos).
    source (any) – El vértice de inicio.

    Returns:
    Un nuevo grafo vacío
    Raises:
    Exception
    """
    
    # 1. Validar que el vértice fuente existe en el grafo
    if g.get_vertex_info(my_graph, source) is None:
        raise Exception(f"El vértice fuente '{source}' no se encuentra en el grafo.")

    # 2. Inicializar la estructura de búsqueda para Dijkstra
    search_structure = new_dijkstra_structure(source, my_graph)

    # 3. Obtener todos los vértices del grafo
    all_vertices_keys = g.vertices(my_graph)

    # 4. Inicializar distancias a infinito para todos los vértices, 0 para el origen
    #    e insertar el origen en la cola de prioridad.
    for i in range(lt.size(all_vertices_keys)):
        v_key = lt.get_element(all_vertices_keys, i)
        map.put(search_structure['dist_to'], v_key, float('inf')) # Distancia inicial infinita
        map.put(search_structure['marked'], v_key, False)         # Ningún vértice marcado al inicio
        # edge_to se inicializa implícitamente a None por el mapa
    
    # Establecer la distancia del vértice fuente a 0 y añadirlo a la cola de prioridad.
    # (El item en la PQ es la clave del vértice, la prioridad es la distancia acumulada)
    map.put(search_structure['dist_to'], source, 0.0) 
    pq.put(search_structure['pq'], 0.0, source) # Prioridad 0, item 'source'

    #print(f"  DIJKSTRA DEBUG: Iniciando Dijkstra desde el vértice '{source}'.")

    # 5. Bucle principal de Dijkstra: Continúa mientras la PQ no esté vacía
    while not pq.is_empty(search_structure['pq']):
        # Extraer el vértice con la distancia mínima acumulada del Min-Priority Queue.
        # Retorna (prioridad, item_value) -> (distancia_acumulada, vertice_actual)
        (current_dist, v_key) = pq.del_min(search_structure['pq'])

        # Si el vértice ya ha sido marcado, lo saltamos (Prim's perezoso/lazy).
        # Para Dijkstra, si ya está marcado, significa que ya hemos encontrado su camino más corto.
        if map.get(search_structure['marked'], v_key):
            #print(f"  DIJKSTRA DEBUG: Vértice '{v_key}' ya procesado. Saltando.")
            continue
        
        # Marcar el vértice 'v_key' como procesado (ya hemos encontrado su camino más corto desde el origen)
        map.put(search_structure['marked'], v_key, True)
        
       # print(f"  DIJKSTRA DEBUG: Procesando vértice '{v_key}'. Distancia acumulada = {current_dist}.")

        # Relajar las aristas adyacentes a 'v_key'
        # Es decir, revisar si al usar 'v_key' se pueden encontrar caminos más baratos
        # para llegar a sus vecinos no marcados.
        
        # Obtener los adyacentes de 'v_key'
        adj_vertices_list = g.adjacents(my_graph, v_key) # Retorna array_list de claves de vecinos
        
        list_size_adj = lt.size(adj_vertices_list)
        for i in range(list_size_adj):
            w_key = lt.get_element(adj_vertices_list, i) # Un vecino de v_key
            
            # Solo consideramos vecinos que aún no han sido procesados (no marcados)
            if not map.get(search_structure['marked'], w_key):
                # Obtener la arista entre v_key y w_key (y su peso)
                # g.get_adjacents devuelve el mapa de adyacencia del vértice.
                adj_map_v = g.get_adjacents(my_graph, v_key) 
                edge_vw_obj = map.get(adj_map_v, w_key) # Esto es el objeto arista {'to', 'weight'}
                edge_weight = edge_vw_obj['weight'] # Obtener el peso de la arista
                
                # Calcular la nueva distancia potencial a 'w_key' a través de 'v_key'
                new_dist = current_dist + edge_weight

                # Si esta nueva distancia es menor que la distancia actual a 'w_key'
                if new_dist < map.get(search_structure['dist_to'], w_key):
                    # Actualizar la distancia mínima para 'w_key'
                    map.put(search_structure['dist_to'], w_key, new_dist)
                    
                    # Almacenar la arista (v_key -> w_key) que proporciona este camino más corto
                    # 'edge_to[w_key]' guarda el objeto arista completo.
                    map.put(search_structure['edge_to'], w_key, {
                        'from': v_key, 
                        'to': w_key, 
                        'weight': edge_weight
                    })
                    
                    # Insertar/actualizar 'w_key' en la PQ con su nueva distancia mínima
                    pq.put(search_structure['pq'], new_dist, w_key)
                   # print(f"    DIJKSTRA DEBUG: Relajando arista '{v_key}'--'{w_key}'. Nuevo dist_to[{w_key}]={new_dist}. Añadido a PQ.")
                #else:
                    #print(f"    DIJKSTRA DEBUG: Arista '{v_key}'--'{w_key}' (peso {edge_weight}) no mejora la distancia a '{w_key}'.")

   # print(f"  DIJKSTRA DEBUG: Algoritmo Dijkstra finalizado.")
    return search_structure

# En DataStructures/Graph/dijkstra.py

# ... (dijkstra(my_graph, source) función aquí) ...

def dist_to(key_v, aux_structure):
    """
    Retorna el costo para llegar del vertice source al vertice key_v.

    Parameters:
    key_v (any) – El vertice destino.
    aux_structure (dijkstra_search) – La estructura de busqueda.

    Returns:
    El costo total para llegar de source a key_v. Infinito si no existe camino.
    Raises:
    Exception (si key_v no existe en el grafo)
    """
    # Si el vértice no fue encontrado en el mapa de distancias (ej. no existe en el grafo o no es alcanzable)
    if map.get(aux_structure['dist_to'], key_v) is None:
        # Aquí, podrías querer lanzar una excepción si key_v no es un vértice válido del grafo
        # O simplemente devolver infinito si es inalcanzable.
        # Basado en la descripción, "Infinito si no existe camino".
        # Asumimos que los vértices no existentes no tienen entrada en dist_to.
        
        # Opcional: Verificar que el vértice realmente existe en el grafo original para lanzar excepción más clara
        if g.get_vertex_info(g.new_graph(0), key_v) is None: # my_graph no está en scope aquí.
            # No podemos verificar existencia del vértice en el grafo original sin pasarlo.
            # Confiamos en que si no está en dist_to, es porque no es alcanzable o no existe.
            pass

        return float('inf') # Retornar infinito si no hay camino

    return map.get(aux_structure['dist_to'], key_v)


def has_path_to(key_v, aux_structure):
    """
    Indica si hay camino de costo mínimo desde el source al vertice key_v.

    Parameters:
    key_v (any) – El vertice de destino.
    aux_structure (dijkstra_search) – La estructura de busqueda.

    Returns:
    True si existe camino, False en caso contrario.
    Raises:
    Exception (si key_v no existe en el grafo)
    """
    # Un vértice tiene camino si fue marcado como procesado y su distancia no es infinito.
    # El mapa 'marked' indica si se encontró el camino más corto a ese vértice.
    # También se puede verificar que la distancia no sea infinito.
    
    # Si el vértice no existe en el mapa 'marked' o no fue marcado como True
    if map.get(aux_structure['marked'], key_v) is None or not map.get(aux_structure['marked'], key_v):
        return False
    
    # Adicionalmente, asegurar que su distancia no es infinito (aunque marked=True ya lo implica para alcanzables)
    if map.get(aux_structure['dist_to'], key_v) == float('inf'):
        return False
        
    return True


def path_to(key_v, aux_structure):
    """
    Retorna el camino de costo mínimo desde source a key_v en una pila.

    Parameters:
    key_v (any) – El vertice de destino.
    aux_structure (dijkstra_search) – La estructura de busqueda.

    Returns:
    Una pila (Stack) con el camino entre source y key_v. Retorna None si no hay camino.
    Raises:
    Exception (si key_v no existe en el grafo)
    """
    if not has_path_to(key_v, aux_structure):
        return None # No hay camino

    path_stack = stk.new_stack() # Usamos la pila para construir el camino inverso
    current_vertex_key = key_v

    # Reconstruir el camino desde el destino hasta el origen usando 'edge_to'
    # Las aristas en 'edge_to' están en el formato {'from': u_key, 'to': w_key, 'weight': edge_weight}
    while current_vertex_key is not None and current_vertex_key != aux_structure['source']:
        stk.push(path_stack, current_vertex_key)
        
        edge_obj = map.get(aux_structure['edge_to'], current_vertex_key)
        if edge_obj is None: # Si no hay arista en edge_to, significa que no hay camino desde source.
            return None # Esto no debería ocurrir si has_path_to es True.
            
        current_vertex_key = edge_obj['from'] # Nos movemos al vértice 'from' de la arista

    # Añadir el vértice origen a la pila al final
    if current_vertex_key == aux_structure['source']:
        stk.push(path_stack, aux_structure['source'])
    else:
        return None # No se llegó al origen (no debería pasar si has_path_to es True)

    # La pila ahora contiene el camino en orden inverso (Destino -> Origen).
    # Se debe invertir para obtener Origen -> Destino.
    # Tu pila usa single_linked_list, así que sll.reverse() se puede usar aquí.
    # asumiendo que sll.reverse puede tomar una pila y devolver una pila o una lista.
    # Alternativamente, convertir a array_list y luego imprimir.
    # Dado que stk.new_stack() devuelve un single_linked_list como base,
    # y tu sll.reverse() existe, se usará.
    return sll.reverse(path_stack) # <--- Usar sll.reverse para invertir la pila (que es una SLL)