# DataStructures/Graph/no_digraph.py

from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Graph import vertex as ver
from DataStructures.Graph import edge as edg 



def new_graph (order, directed=False):
    graph = {
        "directed": directed,
        "order": 0, 
        "num_edges": 0,
        "vertices": None,        
        "adjacency_list": None    
    }
   
    graph["vertices"] = map.new_map(order, 0.5)
    graph["adjacency_list"] = map.new_map(order, 0.5)
    
    return graph

def insert_vertex (my_graph, key_u, info_u):
    my_graph['vertices'] = map.put(my_graph['vertices'], key_u, info_u)
    empty_adj_map = map.new_map(1, 0.5)
    my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, empty_adj_map)
    my_graph['order'] += 1
    return my_graph

def update_vertex_info (my_graph, key_u, new_info_u):
    if map.get(my_graph['vertices'], key_u) is None:
        return None
    else:
        my_graph['vertices'] = map.put(my_graph['vertices'], key_u, new_info_u)
    return my_graph

def add_edge (my_graph, key_u, key_v, weight):
    """
    Adds an edge from vertex key_u to vertex key_v with a given weight.
    key_u: Key of the source vertex.
    key_v: Key of the destination vertex.
    weight: Weight of the edge.
    """
    # Check if both vertices exist
    if map.get(my_graph['vertices'], key_u) is None:
        raise Exception(f"El vertice {key_u} (source) no existe.")
    if map.get(my_graph['vertices'], key_v) is None:
        raise Exception(f"El vertice {key_v} (destination) no existe.")

    # --- FIX START: Determine if edge(s) existed BEFORE any map.put in this call ---

    # Get the current adjacency map for vertex u
    adj_map_for_u_before_put = map.get(my_graph['adjacency_list'], key_u)
    # Check if the u->v edge already existed (will be False if adj_map_for_u_before_put is None)
    edge_u_v_existed_before = False
    if adj_map_for_u_before_put is not None:
        edge_u_v_existed_before = map.get(adj_map_for_u_before_put, key_v) is not None

    # Get the current adjacency map for vertex v (needed for undirected reverse check)
    adj_map_for_v_before_put = map.get(my_graph['adjacency_list'], key_v)
    edge_v_u_existed_before = False # Flag for the reverse edge in undirected graphs
    if not my_graph['directed'] and adj_map_for_v_before_put is not None: # Only check if undirected
        edge_v_u_existed_before = map.get(adj_map_for_v_before_put, key_u) is not None

    # --- FIX END: Existence flags are now correctly captured ---

    # --- Add the u->v edge ---
    adj_map_for_u = adj_map_for_u_before_put # Use the retrieved map reference
    if adj_map_for_u is None: # If the map for u didn't exist, create it
        adj_map_for_u = map.new_map(1, 0.5)
        my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, adj_map_for_u)
    
    new_edge_uv = edg.new_edge(key_v, weight) # Create the edge object
    updated_adj_map_for_u = map.put(adj_map_for_u, key_v, new_edge_uv) # Add/update edge in u's map
    my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_u, updated_adj_map_for_u) # Update main graph's reference

    # --- If the graph is undirected, add the reverse edge (v->u) ---
    if not my_graph['directed']:
        adj_map_for_v = adj_map_for_v_before_put # Use the retrieved map reference
        if adj_map_for_v is None: # If the map for v didn't exist, create it
            adj_map_for_v = map.new_map(1, 0.5)
            my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_v, adj_map_for_v)
        
        new_edge_vu = edg.new_edge(key_u, weight) # Create reverse edge object
        updated_adj_map_for_v = map.put(adj_map_for_v, key_u, new_edge_vu) # Add/update edge in v's map
        my_graph['adjacency_list'] = map.put(my_graph['adjacency_list'], key_v, updated_adj_map_for_v) # Update main graph's reference
        
        # --- FIX START: Increment num_edges based on BEFORE existence ---
        # For an undirected graph, num_edges increments only if the conceptual edge (u,v)
        # did not exist in either direction before this call.
        if not edge_u_v_existed_before and not edge_v_u_existed_before:
             my_graph['num_edges'] += 1
        # --- FIX END ---
    else: # For directed graphs
        # For directed, increment num_edges only if the specific u->v edge didn't exist before.
        if not edge_u_v_existed_before:
             my_graph['num_edges'] += 1
    
    return my_graph

def order(my_graph):
    return my_graph['order']

def size(my_graph):
    return my_graph['num_edges']

def vertices(my_graph):
    return map.key_set(my_graph['vertices'])

def degree(my_graph, key_u):
    if map.get(my_graph['vertices'], key_u) is None:
        raise Exception(f"El vertice {key_u} no existe.")
    adj_map_for_u = map.get(my_graph['adjacency_list'], key_u)
    if adj_map_for_u is None:
        return 0
    return map.size(adj_map_for_u)

# As per your assignment, this function remains exactly as is.
def out_degree(my_graph,key_u):
    lista_adyacencia_u = map.get(my_graph['vertices'],key_u)
    if lista_adyacencia_u == None:
        raise Exception("El vertice no existe")
    numero = lista_adyacencia_u['adjacents']['size']     
    return numero


def get_adjacents(my_graph, vertex_key):

    if map.get(my_graph['vertices'], vertex_key) is None:
        return None
    adj_map = map.get(my_graph['adjacency_list'], vertex_key)
    
    if adj_map is None:
        return map.new_map(1, 0.5) 
    
    return adj_map 


def adjacents(my_graph, vertex_key):

    adj_map = get_adjacents(my_graph, vertex_key) 
    
    if adj_map is None: 
        return lt.new_list() 

    return map.key_set(adj_map)

def get_vertex_info(my_graph, key_u):
    return map.get(my_graph['vertices'], key_u)