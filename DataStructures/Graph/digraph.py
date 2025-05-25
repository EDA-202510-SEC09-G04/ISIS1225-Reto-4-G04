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

def update_vertex_info(my_graph, key_u, new_info_u):
    my_graph["vertices"] = map.put(my_graph["vertices"], key_u, new_info_u)
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

def add_edge(my_graph, key_u, key_v, weight=1.0):
    if not contains_vertex(my_graph, key_u):
        raise Exception("El vertice u no existe")
    if not contains_vertex(my_graph, key_v):
        raise Exception("El vertice v no existe")

    # Obtener el vertice origen
    u_entry = map.get(my_graph['vertices'], key_u)
    
    # Si no tiene adjacents, inicializarlo como mapa
    if 'adjacents' not in u_entry:
        u_entry['adjacents'] = map.new_map(num_elements=2, load_factor=0.5)
    
    # Verificar si ya existe el arco
    existing_edge = map.get(u_entry['adjacents'], key_v)
    if existing_edge is None:
        my_graph['num_edges'] += 1
    
    # Agregar/actualizar el arco
    edge_info = {'to': key_v, 'weight': weight}
    map.put(u_entry['adjacents'], key_v, edge_info)
    
    return my_graph


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
    
    vertex = get_vertex(my_graph, key_u)
    # Eliminamos 'edges' para solo retornar la información del vértice
    return {k: v for k, v in vertex.items() if k != 'edges'}

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
        raise Exception("El vertice no existe")

    vertex_value = map.get(my_graph['vertices'], key_u)
    
    vertex = {
        'key': key_u,  
        'value': vertex_value['value'], 
        'adjacents': []
    }

    if 'adjacents' in vertex_value:
        adj_keys = map.key_set(vertex_value['adjacents'])
        for key_v in adj_keys:
            edge = map.get(vertex_value['adjacents'], key_v)
            vertex['adjacents'].append({
                'to': key_v,
                'weight': edge['weight']
            })

    return vertex


