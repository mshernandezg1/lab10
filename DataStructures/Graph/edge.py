def new_edge(v_a, v_b, weight=0):
    """
    Crea un nuevo arco entrelos vertices ''v_a'' y ''v_b'' con un peso ''weight''

    Se crea un arco con los siguientes atributos:

    - **vertex_a**: Vertice A del arco
    - **vertex_b**: Vertice B del arco
    - **weight**: Peso del arco

    :param v_a: Vertice A del arco
    :type v_a: any
    :param v_b: Vertice B del arco
    :type v_b: any
    :param weight: Peso del arco
    :type weight: double

    :returns: Arco creado
    :rtype: edge
    """
    edge = {"vertex_a": v_a, "vertex_b": v_b, "weight": weight}
    return edge


def weight(edge):
    """
    Retorna el peso del arco ''edge''

    :param edge: Arco del cual se quiere obtener el peso
    :type edge: edge

    :returns: Peso del arco
    :rtype: double
    """
    return edge["weight"]


def either(edge):
    """
    Retorna el vertice A del arco ''edge''

    :param edge: Arco del cual se quiere obtener el vertice A
    :type edge: edge

    :returns: Vertice A del arco
    :rtype: any
    """
    return edge["vertex_a"]


def other(edge, veither):
    """
    Retorna el vertice B del arco

    :param edge: Arco del cual se quiere obtener el vertice B
    :type edge: edge
    :param veither: Vertice A del arco
    :type veither: any

    :returns: Vertice B del arco
    :rtype: any
    """
    if veither == edge["vertex_a"]:
        return edge["vertex_b"]
    elif veither == edge["vertex_b"]:
        return edge["vertex_a"]


def set_weight(edge, weight):
    """
    Cambia el peso del arco ''edge'' por el valor ''weight''

    :param edge: Arco al cual se le quiere cambiar el peso
    :type edge: edge
    :param weight: Nuevo peso del arco
    :type weight: double
    """
    edge["weight"] = weight


def compare_edges(edge1, edge2):
    """
    Funcion utilizada en lista de edges para comparar dos edges
    Retorna 0 si los arcos son iguales, 1 si edge1 > edge2, -1 edge1 < edge2

    :param edge1: Arco 1
    :type edge1: edge
    :param edge2: Arco 2
    :type edge2: edge

    :returns: 0 si los arcos son iguales, 1 si edge1 > edge2, -1 edge1 < edge2
    :rtype: int
    """
    e1v = either(edge1)
    e2v = either(edge2)

    if e1v == e2v:
        if other(edge1, e1v) == other(edge2, e2v):
            return 0
        elif other(edge1, e1v) > other(edge2, e2v):
            return 1
        else:
            return -1
    elif e1v > e2v:
        return 1
    else:
        return -1
