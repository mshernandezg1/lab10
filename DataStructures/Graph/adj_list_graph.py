from edge import new_edge, other
def new_graph():
    return {"vertices": {}, "edges": []}

def insert_vertex(graph, key_vertex, info_vertex):
    if key_vertex not in graph["vertices"]:
        graph["vertices"][key_vertex] = {"info": info_vertex, "adjacent": []}

def add_edge(graph, vertex_a, vertex_b, weight=0):
    if vertex_a in graph["vertices"] and vertex_b in graph["vertices"]:
        edge = new_edge(vertex_a, vertex_b, weight)
        graph["edges"].append(edge)
        graph["vertices"][vertex_a]["adjacent"].append(edge)
        graph["vertices"][vertex_b]["adjacent"].append(edge)

def get_edge(graph, vertex_a, vertex_b):
    for edge in graph["vertices"][vertex_a]["adjacent"]:
        if other(edge, vertex_a) == vertex_b:
            return edge
    return None

def contains_vertex(graph, vertex):
    return vertex in graph["vertices"]
