from pprint import pprint
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Map import map_entry as me


def new_graph(order, load_factor=0.5):
    """Crea un grafo con una estructura clara"""
    return {
        'vertices': mp.new_map(num_elements=order, load_factor=load_factor),
        'num_edges': 0,
        'directed': False  # Añadir este flag para claridad
    }

def insert_vertex(my_graph, key, info):
    """Inserta un vértice correctamente"""
    if not isinstance(info, dict):
        info = {'value': info}  # Asegurar estructura mínima
    
    # Inicializar estructura del vértice
    vertex_data = {
        'info': info,
        'adjacents':mp.new_map(num_elements=2, load_factor=0.5)
    }
    
    # Insertar usando el mapa
    my_graph['vertices'] = mp.put(my_graph['vertices'], key, vertex_data)
    return my_graph

def update_vertex_info(my_graph, key_u, new_info):
    if not contains_vertex(my_graph, key_u):
        raise Exception("Vértice no encontrado")
    
    # Conservar la estructura de adyacentes si existe
    current = mp.get(my_graph['vertices'], key_u)
    if 'adjacents' in current:
        new_info['adjacents'] = current['adjacents']
    
    mp.put(my_graph['vertices'], key_u, new_info)
    return my_graph

def remove_vertex(my_graph, key_u):
    # Eliminar el vértice principal
    my_graph["vertices"] = mp.remove(my_graph["vertices"], key_u)
    
    # Eliminar todas las aristas que apuntan a este vértice
    vertices = mp.key_set(my_graph["vertices"])
    for key_v in vertices:
        v_entry = mp.get(my_graph["vertices"], key_v)
        if 'adjacents' in v_entry:
            if mp.contains(v_entry['adjacents'], key_u):
                mp.remove(v_entry['adjacents'], key_u)
                my_graph['num_edges'] -= 1
    return my_graph

def add_edge(my_graph, u, v, weight, undirected=False):
    # Verificar si la arista ya existe
    if has_edge(my_graph, u, v) or (undirected and has_edge(my_graph, v, u)):
        return my_graph  # No hacer nada si ya existe

    # Añadir arista u→v
    u_entry = mp.get(my_graph['vertices'], u)
    u_entry['adjacents'] = mp.put(u_entry['adjacents'], v, weight)
    
    # Si es no dirigido, añadir v→u (pero no contar como nueva arista)
    if undirected:
        v_entry = mp.get(my_graph['vertices'], v)
        v_entry['adjacents'] = mp.put(v_entry['adjacents'], u, weight)
    
    # Contar como 1 arista siempre (incluso para no dirigido)
    my_graph['num_edges'] += 1
    return my_graph

def insert_directed_edge(my_graph, key_u, key_v, weight):
    u_entry = mp.get(my_graph['vertices'], key_u)

    if 'adjacents' not in u_entry:
        u_entry['adjacents'] = mp.new_map(num_elements=2, load_factor=0.5)

    # Verificar si ya existe el arco
    existing_edge = mp.get(u_entry['adjacents'], key_v)
    if existing_edge is None:
        my_graph['num_edges'] += 1

    edge_info = {'to': key_v, 'weight': weight}
    mp.put(u_entry['adjacents'], key_v, edge_info)

def has_edge(my_graph, key_u, key_v):
    u_entry = mp.get(my_graph['vertices'], key_u)
    return (u_entry is not None and 
            'adjacents' in u_entry and 
            mp.contains(u_entry['adjacents'], key_v))


def order(my_graph):
    return mp.size(my_graph['vertices'])

def size(my_graph):
    return my_graph['num_edges']

def vertices(my_graph):
    vertex_keys = mp.key_set(my_graph['vertices'])
    return vertex_keys

def degree(my_graph, key_u):
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice no existe")
    
    vertex_entry = mp.get(my_graph['vertices'], key_u)
    if 'adjacents' not in vertex_entry:
        return 0
        
    return mp.size(vertex_entry['adjacents'])

def get_edge(my_graph, key_u, key_v):
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice u no existe")
    
    u_entry = mp.get(my_graph['vertices'], key_u)
    if 'adjacents' not in u_entry:
        return None
        
    edge = mp.get(u_entry['adjacents'], key_v)
    return edge

def get_vertex_information(my_graph, key_u):
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice no existe")
    
    vertex_entry = mp.get(my_graph['vertices'], key_u)
    return vertex_entry  # Devuelve directamente la entrada del mpa

def contains_vertex(my_graph, key_u):
    return mp.contains(my_graph['vertices'], key_u)


def adjacents(my_graph, key_u):
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice no existe")
    
    u_entry = mp.get(my_graph['vertices'], key_u)
    if 'adjacents' not in u_entry:
        return []
        
    return mp.key_set(u_entry['adjacents'])

def edges_vertex(my_graph, key_u):
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice no existe")

    u_entry = mp.get(my_graph['vertices'], key_u)
    edges_list = []

    if 'adjacents' in u_entry:
        adj_keys = mp.key_set(u_entry['adjacents'])
        for key_v in adj_keys:
            edge = mp.get(u_entry['adjacents'], key_v)
            edges_list.append((key_u, key_v, edge['weight']))

    return edges_list

def get_vertex(my_graph, key_u):
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vértice no existe")

    vertex_entry = mp.get(my_graph['vertices'], key_u)
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
        adj_keys = mp.key_set(adj_map)

        for key_v in adj_keys:
            edge = mp.get(adj_map, key_v)
            if edge is not None:
                vertex['adjacents'].append({
                    'to': key_v,
                    'weight': edge['weight']
                })

    return vertex

