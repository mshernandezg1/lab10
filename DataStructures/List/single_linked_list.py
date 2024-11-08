from DataStructures.List import list_node as nd 

def new_list(): 
    newlist = {"first": None, 
               "last": None,
               "size": 0}
    return newlist


def add_first(my_list, element): 
    newnode = nd.new_single_node(element)
    if my_list["first"] is None: 
        my_list["first"] = newnode
        my_list["last"] = newnode
    else: 
        newnode["next"] = my_list["first"]
        my_list["first"] = newnode
    my_list["size"] += 1 
    return my_list
 

def add_last(my_list, element):
    newnode = nd.new_single_node(element)
    if my_list["first"] is None: 
        my_list["first"] = newnode
        my_list["last"] = newnode 
    else: 
        my_list["last"]["next"] = newnode
        my_list["last"] = newnode
    my_list["size"] += 1 
    return my_list

def is_empty(my_list): 
    vacia = None 
    if my_list["size"] ==0: 
        vacia = True 
    else: 
        vacia = False 
    return vacia 
 
def size(my_list): 
    return my_list["size"]

def first_element(my_list): 
    return my_list["first"]["info"]  

def last_element(my_list): 
    return my_list["last"]["info"]  

def get_element(my_list, pos): 
    if (pos < 0) or (pos >= my_list["size"]) or (my_list["first"] is None):
        return None 
    actual = my_list["first"]
    pos_actual = 0 
    
    while pos_actual < pos: 
        actual = actual["next"]
        pos_actual += 1
    return actual["info"] 
def remove_first(my_list):

    if my_list["first"] == my_list["last"]: 
        my_list["first"] = None
        my_list["last"] = None
    else:
        my_list["first"] = my_list["first"]["next"]
    my_list["size"] -= 1
    return my_list

def remove_last(my_list):
    if my_list["first"] == my_list["last"]:  
        my_list["first"] = None
        my_list["last"] = None
    else:
        actual = my_list["first"]
        while actual["next"] != my_list["last"]:
            actual = actual["next"]
        actual["next"] = None
        my_list["last"] = actual
    my_list["size"] -= 1
    return my_list

def insert_element(my_list, element, pos):
    if pos < 0 or pos > my_list["size"]:
        return my_list
    if pos == 0:
        return add_first(my_list, element)
    elif pos == my_list["size"]:
        return add_last(my_list, element)
    else:
        actual = my_list["first"]
        contador = 0
        while contador < pos - 1:
            actual = actual["next"]
            contador += 1
        nuevo_nodo = nd.new_single_node(element)
        nuevo_nodo["next"] = actual["next"]
        actual["next"] = nuevo_nodo
        my_list["size"] += 1
    return my_list

def is_present(my_list, element, cmp_function):
    actual = my_list["first"]
    posicion = -1
    contador = 0
    while actual is not None:
        if cmp_function(actual["info"], element) == 0:
            posicion = contador
            break
        actual = actual["next"]
        contador += 1
    return posicion

def delete_element(my_list, pos):
    actual = my_list["first"]
    previo = None

    if pos >= 0 and pos < my_list["size"]:
        for _ in range(pos):
            previo = actual
            actual = actual["next"]

        if previo is None: 
            my_list["first"] = actual["next"]
            if my_list["first"] is None:
                my_list["last"] = None
        else:
            previo["next"] = actual["next"]
            if previo["next"] is None:
                my_list["last"] = previo
        my_list["size"] -= 1
    
    return my_list
            
def change_info(my_list, pos, info):
    if pos >= 0 and pos < my_list["size"]:
        actual = my_list["first"]
        contador = 0
        while contador < pos:
            actual = actual["next"]
            contador += 1
        actual["info"] = info
    return my_list


def exchange(my_list, pos1, pos2):
    nodo1 = get_node_at(my_list, pos1)
    nodo2 = get_node_at(my_list, pos2)
    
    nodo1["info"], nodo2["info"] = nodo2["info"], nodo1["info"]
    
    return my_list


def sub_list(my_list, pos, num_elem):
    """
    Creates a deep copy sublist from position `pos` with `num_elem` elements.
    """
    sublista = {"first": None, "last": None, "size": 0}

    if pos < 0 or pos >= my_list["size"]:
        return sublista  

    actual = my_list["first"]
    contador = 0
    while contador < pos and actual is not None:
        actual = actual["next"]
        contador += 1
    while num_elem > 0 and actual is not None:
        add_last(sublista, actual["info"])
        actual = actual["next"]
        num_elem -= 1

    return sublista

def merge_sort(my_list, sort_crit):
    tamanio = size(my_list)
    
    if tamanio > 1:
        mid = tamanio // 2
        left_half = sub_list(my_list, 0, mid)
        right_half = sub_list(my_list, mid, tamanio - mid)
        merge_sort(left_half, sort_crit)
        merge_sort(right_half, sort_crit)
        
        i = j = k = 0
        left_size = size(left_half)
        right_size = size(right_half)

        while i < left_size and j < right_size:
            left_element = get_node_at(left_half, i)
            right_element = get_node_at(right_half, j)
            if sort_crit(left_element["info"], right_element["info"]):
                change_info(my_list, k, left_element["info"])
                i += 1
            else:
                change_info(my_list, k, right_element["info"])
                j += 1
            k += 1

        while i < left_size:
            left_element = get_node_at(left_half, i)
            change_info(my_list, k, left_element["info"])
            i += 1
            k += 1

        while j < right_size:
            right_element = get_node_at(right_half, j)
            change_info(my_list, k, right_element["info"])
            j += 1
            k += 1

    return my_list




def get_node_at(my_list, pos):
    """
    Devuelve el nodo en la posición `pos`.
    """
    actual = my_list["first"]
    pos_actual = 0
    
    while pos_actual < pos:
        actual = actual["next"]
        pos_actual += 1
    return actual

def selection_sort(my_list, sort_crit):
    tamanio = size(my_list)
    
    for i in range(tamanio):
        min_index = i
        min_node = get_node_at(my_list, min_index)
        
        for j in range(i + 1, tamanio):
            current_node = get_node_at(my_list, j)
            if not sort_crit(min_node["info"], current_node["info"]):
                min_index = j
                min_node = current_node
        if min_index != i:
            exchange(my_list, i, min_index)            
    return my_list