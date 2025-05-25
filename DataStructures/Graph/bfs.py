from DataStructures.Graph import digraph as G
from DataStructures.List import single_linked_list as lt

def bfs(graph, start_vertex):
    from collections import deque
    visited = {}
    queue = deque()
    path = []

    visited[start_vertex] = True
    queue.append(start_vertex)

    while queue:
        v = queue.popleft()
        path.append(v)
        adj = G.adjacents(graph, v)
        while not lt.is_empty(adj):
            neighbor = lt.remove_first(adj)
            if not visited.get(neighbor, False):
                visited[neighbor] = True
                queue.append(neighbor)
    return path