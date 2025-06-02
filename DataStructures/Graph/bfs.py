

from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt 
from DataStructures.Graph import digraph as g 
from DataStructures.Queue import queue as Q 



def bfs(my_graph, source):
    """
    Performs a Breadth-First Search (BFS) starting from a source vertex.
    Calculates reachability, shortest paths (in terms of number of edges),
    and distances from the source.

    Args:
        my_graph: The graph object (from no_digraph.py).
        source: The key of the starting vertex for BFS.

    Returns:
        A dictionary containing BFS search data:
        - 'visited': A map (map_linear_probing) storing {'marked': True/False, 'edgeTo': predecessor_key, 'dist': distance_from_source}
        - 'source': The key of the source vertex.
    """
    # 1. Check if the source vertex exists in the graph
    if g.get_vertex_info(my_graph, source) is None:
        raise ValueError(f"Source vertex {source} not found in graph.")

    order = g.order(my_graph)

    # 2. Initialize visited map to store search data
    # Each entry will be {vertex_key: {'marked': bool, 'edgeTo': predecessor_key, 'dist': int}}
    search_data = {
        'visited': map.new_map(order, 0.5), # Map to store visited status and path info
        'source': source # Store the source vertex key
    }

    # 3. Create a queue for BFS traversal
    bfs_queue = Q.new_queue()

    # 4. Mark the source node as visited, set its distance to 0, and enqueue it
    map.put(search_data['visited'], source, {'marked': True, 'edgeTo': None, 'dist': 0})
    Q.enqueue(bfs_queue, source)


    # 5. Main BFS loop: Continues as long as there are vertices in the queue to explore
    while not Q.is_empty(bfs_queue):
        v = Q.dequeue(bfs_queue) # Dequeue the current vertex to explore its neighbors


        # Get the neighbors of the current vertex 'v'
        # g.adjacents returns an array_list of neighbor keys (e.g., ['B', 'C', 'D'])
        adj_vertex_keys_list = g.adjacents(my_graph, v)

        list_size = lt.size(adj_vertex_keys_list)
        for i in range(list_size):
            w = lt.get_element(adj_vertex_keys_list, i) # Get neighbor 'w'

            visited_info = map.get(search_data['visited'], w)

            # Check if neighbor 'w' has not been visited
            if visited_info is None or not visited_info.get('marked', False):
                # Mark 'w' as visited, record its predecessor, and calculate its distance
                map.put(search_data['visited'], w, {
                    'marked': True,
                    'edgeTo': v,
                    'dist': map.get(search_data['visited'], v)['dist'] + 1 # Distance is one more than predecessor
                })
                Q.enqueue(bfs_queue, w) # Enqueue the newly visited neighbor

            

    return search_data 


# --- Helper functions to query BFS results ---

def hasPathTo(search_data, vertex):
    """
    Checks if there is a path from the source to the given vertex based on BFS results.
    """
    visited_info = map.get(search_data['visited'], vertex)
    return visited_info is not None and visited_info.get('marked', False)


def distTo(search_data, vertex):
    """
    Returns the shortest distance (number of edges) from the source to the given vertex.
    Returns None if the vertex is not reachable.
    """
    if not hasPathTo(search_data, vertex):
        return None
    return map.get(search_data['visited'], vertex)['dist']


def pathTo(search_data, vertex):
    """
    Reconstructs the shortest path from the source to the given vertex using BFS results.
    Returns an array_list of vertex keys, representing the path from source to target.

    Since BFS finds shortest paths in unweighted graphs (number of edges), this pathTo
    will return a shortest path. The path is built by tracing edgeTo backwards from the target
    and then reversed (by using add_first on array_list).
    """
    if not hasPathTo(search_data, vertex):
        return None

    # Path will be built from target back to source using array_list (lt)
    path_array_list_reversed = lt.new_list() 

    current_vertex = vertex
    # Loop back from target to source using edgeTo
    while current_vertex is not None and current_vertex != search_data['source']:
        lt.add_first(path_array_list_reversed, current_vertex) # Add to front to naturally reverse
        visited_info = map.get(search_data['visited'], current_vertex)
        if visited_info is None or 'edgeTo' not in visited_info:
            return None # Should not happen if hasPathTo is True and data is consistent
        current_vertex = visited_info['edgeTo']
    
    # Add the source node to the front
    if current_vertex == search_data['source']:
        lt.add_first(path_array_list_reversed, search_data['source'])
    else:
        return None # Path couldn't reach source (shouldn't happen if hasPathTo is True)

    # The path is now in Source -> Target order in path_array_list_reversed (due to add_first)
    return path_array_list_reversed