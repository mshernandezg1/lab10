from edge import new_edge, other
# adj_list_graph.py
def new_graph():
    # Crea un nuevo grafo vacío
    return {"vertices": {}, "edges": []}

def insert_vertex(graph, key_vertex, info_vertex):
    # Inserta un nuevo vértice en el grafo con una clave y la información asociada
    if key_vertex not in graph["vertices"]:
        graph["vertices"][key_vertex] = {"info": info_vertex, "adjacent": []}

def add_edge(graph, vertex_a, vertex_b, weight=0):
    # Añade una arista entre vertex_a y vertex_b con un peso específico
    if vertex_a in graph["vertices"] and vertex_b in graph["vertices"]:
        edge = new_edge(vertex_a, vertex_b, weight)
        graph["edges"].append(edge)
        graph["vertices"][vertex_a]["adjacent"].append(edge)
        graph["vertices"][vertex_b]["adjacent"].append(edge)

def get_edge(graph, vertex_a, vertex_b):
    # Busca y retorna la arista entre vertex_a y vertex_b
    for edge in graph["vertices"][vertex_a]["adjacent"]:
        if other(edge, vertex_a) == vertex_b:
            return edge
    return None

def contains_vertex(graph, vertex):
    # Verifica si un vértice está en el grafo
    return vertex in graph["vertices"]
