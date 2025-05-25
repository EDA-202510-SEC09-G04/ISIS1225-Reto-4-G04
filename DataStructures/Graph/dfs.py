from DataStructures.Graph import digraph as G
from DataStructures.List import single_linked_list as lt

def dfs(graph, start_vertex):
    visited = {}
    path = []

    def recursive_dfs(v):
        visited[v] = True
        path.append(v)
        adj = G.adjacents(graph, v)
        while not lt.is_empty(adj):
            neighbor = lt.remove_first(adj)
            if not visited.get(neighbor, False):
                recursive_dfs(neighbor)

    recursive_dfs(start_vertex)
    return path