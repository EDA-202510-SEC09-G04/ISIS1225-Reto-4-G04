# DataStructures/Graph/dfs.py

from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt
from DataStructures.Graph import digraph as g 
from DataStructures.Stack import stack as stk
from DataStructures.List import single_linked_list as sll

def dfs(my_graph, source):
    if g.get_vertex_info(my_graph, source) is None:
        raise ValueError(f"Source vertex {source} not found in graph.")

    order = g.order(my_graph)

    search_data = {
        'visited': map.new_map(order, 0.5),
        'source': source
    }

    map.put(search_data['visited'], source, {'marked': True, 'edgeTo': None})
    _dfs_vertex_recursive_helper(search_data, my_graph, source)

    return search_data

def _dfs_vertex_recursive_helper(search, graph, vertex):
    adj_vertex_keys_list = g.adjacents(graph, vertex) 


    list_size = lt.size(adj_vertex_keys_list)
    for i in range(list_size):
        w = lt.get_element(adj_vertex_keys_list, i)

        visited_info = map.get(search['visited'], w)

        if visited_info is None or not visited_info.get('marked', False):
            map.put(search['visited'], w, {'marked': True, 'edgeTo': vertex})
            _dfs_vertex_recursive_helper(search, graph, w)

def hasPathTo(search_data, vertex):
    visited_info = map.get(search_data['visited'], vertex)
    if visited_info and visited_info.get('marked', False):
        return True
    return False

def pathTo(search_data, vertex):
    if not hasPathTo(search_data, vertex):
        return None

    path = stk.new_stack()
    current_vertex = vertex

    if current_vertex == search_data['source']:
        stk.push(path, search_data['source'])
        return path

    while current_vertex is not None and current_vertex != search_data['source']:
        stk.push(path, current_vertex)
        visited_info = map.get(search_data['visited'], current_vertex)
        if visited_info is None or 'edgeTo' not in visited_info:
            return None
        current_vertex = visited_info['edgeTo']

    if current_vertex == search_data['source']:
        stk.push(path, search_data['source'])
    else:
        return None
    
    path = sll.reverse(path)
    

    return path