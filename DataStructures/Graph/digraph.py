from pprint import pprint
from DataStructures.Map import map_linear_probing as map
from DataStructures.Map import map_entry as me


def new_graph(order, load_factor=0.5):
    graph = {
        'vertices': map.new_map(num_elements=order, load_factor=load_factor),
        'num_edges': 0
    }
    return graph

def insert_vertex(my_graph, key_u, info_u):
    map.put(my_graph['vertices'], key_u, info_u)
    return my_graph

def update_vertex_info(my_graph, key_u, new_info):
    if not contains_vertex(my_graph, key_u):
        raise Exception("Vértice no encontrado")
    
    # Conservar la estructura de adyacentes si existe
    current = map.get(my_graph['vertices'], key_u)
    if 'adjacents' in current:
        new_info['adjacents'] = current['adjacents']
    
    map.put(my_graph['vertices'], key_u, new_info)
    return my_graph

def remove_vertex(my_graph, key_u):
    # Eliminar el vértice principal
    my_graph["vertices"] = map.remove(my_graph["vertices"], key_u)
    
    # Eliminar todas las aristas que apuntan a este vértice
    vertices = map.key_set(my_graph["vertices"])
    for key_v in vertices:
        v_entry = map.get(my_graph["vertices"], key_v)
        if 'adjacents' in v_entry:
            if map.contains(v_entry['adjacents'], key_u):
                map.remove(v_entry['adjacents'], key_u)
                my_graph['num_edges'] -= 1
    return my_graph

def add_edge(my_graph, key_u, key_v, weight, undirected=False):
    if not contains_vertex(my_graph, key_u) or not contains_vertex(my_graph, key_v):
        raise Exception("Vértice(s) no existente(s)")

    # Solo incrementar num_edges si es una nueva conexión
    if not has_edge(my_graph, key_u, key_v):
        my_graph['num_edges'] += 1
    insert_directed_edge(my_graph, key_u, key_v, weight)

    if undirected and not has_edge(my_graph, key_v, key_u):
        my_graph['num_edges'] += 1
        insert_directed_edge(my_graph, key_v, key_u, weight)

def insert_directed_edge(my_graph, key_u, key_v, weight):
    u_entry = map.get(my_graph['vertices'], key_u)

    if 'adjacents' not in u_entry:
        u_entry['adjacents'] = map.new_map(num_elements=2, load_factor=0.5)

    # Verificar si ya existe el arco
    existing_edge = map.get(u_entry['adjacents'], key_v)
    if existing_edge is None:
        my_graph['num_edges'] += 1

    edge_info = {'to': key_v, 'weight': weight}
    map.put(u_entry['adjacents'], key_v, edge_info)

def has_edge(my_graph, key_u, key_v):
    if not contains_vertex(my_graph, key_u):
        return False
    
    u_entry = map.get(my_graph['vertices'], key_u)
    return ('adjacents' in u_entry and 
            map.contains(u_entry['adjacents'], key_v))


def order(my_graph):
    return map.size(my_graph['vertices'])

def size(my_graph):
    return my_graph['num_edges']

def vertices(my_graph):
    vertex_keys = map.key_set(my_graph['vertices'])
    return vertex_keys

def degree(my_graph, key_u):
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice no existe")
    
    vertex_entry = map.get(my_graph['vertices'], key_u)
    if 'adjacents' not in vertex_entry:
        return 0
        
    return map.size(vertex_entry['adjacents'])

def get_edge(my_graph, key_u, key_v):
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice u no existe")
    
    u_entry = map.get(my_graph['vertices'], key_u)
    if 'adjacents' not in u_entry:
        return None
        
    edge = map.get(u_entry['adjacents'], key_v)
    return edge['weight'] if edge else None

def get_vertex_information(my_graph, key_u):
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice no existe")
    
    vertex_entry = map.get(my_graph['vertices'], key_u)
    return vertex_entry  # Devuelve directamente la entrada del mapa

def contains_vertex(my_graph, key_u):
    return map.contains(my_graph['vertices'], key_u)


def adjacents(my_graph, key_u):
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice no existe")
    
    u_entry = map.get(my_graph['vertices'], key_u)
    if 'adjacents' not in u_entry:
        return []
        
    return map.key_set(u_entry['adjacents'])

def edges_vertex(my_graph, key_u):
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice no existe")

    u_entry = map.get(my_graph['vertices'], key_u)
    edges_list = []

    if 'adjacents' in u_entry:
        adj_keys = map.key_set(u_entry['adjacents'])
        for key_v in adj_keys:
            edge = map.get(u_entry['adjacents'], key_v)
            edges_list.append((key_u, key_v, edge['weight']))

    return edges_list

def get_vertex(my_graph, key_u):
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vértice no existe")

    vertex_entry = map.get(my_graph['vertices'], key_u)
    if vertex_entry is None:
        raise Exception(f"No se encontró el vértice con clave: {key_u}")
    
    vertex_value = vertex_entry

    vertex = {
        'key': key_u,
        'value': vertex_value,
        'adjacents': []
    }

    if 'adjacents' in vertex_value and 'table' in vertex_value['adjacents']:
        adj_map = vertex_value['adjacents']
        adj_keys = map.key_set(adj_map)

        for key_v in adj_keys:
            edge = map.get(adj_map, key_v)
            if edge is not None:
                vertex['adjacents'].append({
                    'to': key_v,
                    'weight': edge['weight']
                })

    return vertex

