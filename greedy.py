positions = [(1, 6, 10), (2, 0, 5), (3, 5, 8), (4, 8, 4)]


def greedy(vertices):
    visited = [False for _ in range(len(vertices))]
    visited[0] = True
    current_vertex = vertices[0]
    path = [current_vertex]
    while len(path) < len(vertices):
        min_dist = None
        closest_vertex = None
        closest_vertex_index = None
        for i in range(len(vertices)):
            vertex = vertices[i]
            if vertex == current_vertex or visited[i]:
                continue
            dist = ((current_vertex[1] - vertex[1]) ** 2 + (current_vertex[2] - vertex[2]) ** 2) ** (1 / 2)
            if min_dist is None or min_dist > dist:
                min_dist = dist
                closest_vertex = vertex
                closest_vertex_index = i
        path.append(closest_vertex)
        visited[closest_vertex_index] = True
        current_vertex = closest_vertex
    return path
