def new_list():
    newlist = {'elements': [],
               'size': 0}
    return newlist 

def get_element(my_list, pos):
    return my_list["elements"][pos-1]

def is_present(my_list, element, cmp_function): 
    size = my_list["size"]
    if size >0: 
        keyexist = False 
        for keypos in range(0, size): 
            info = my_list["elements"][keypos]
            if (cmp_function(element, info) ==0): 
                keyexist= True 
                break 
        if keyexist: 
           return keypos 
    return -1

def add_first(my_list, element): 
    my_list["elements"].insert(0, element)
    my_list["size"]+= 1 
    return my_list 

def add_last(my_list, element): 
    my_list['elements'].append(element)
    my_list['size'] += 1
    return my_list 

def size(my_list): 
    return my_list["size"]
    
def is_empty(my_list): 
    if (my_list["size"]==0): 
        return True 
    else: 
        return False 
    
def first_element(my_list): 
    return my_list["elements"][0]

def last_element(my_list): 
    posicion = my_list["size"]- 1
    return my_list["elements"][posicion]

def get_element(my_list, pos): 
     if my_list["size"] >0: 
         element = my_list["elements"][pos-1]
         return element 

def remove_first(my_list): 
    if my_list["size"] >0: 
        my_list["elements"].pop(0)
        my_list["size"] -= 1 
    return my_list 
    
def remove_last(my_list): 
    if my_list["size"]>0: 
        elemento_final = my_list["elements"].pop(my_list["size"]-1)
        my_list["size"] -= 1
    else: 
        elemento_final = None  
    return elemento_final 

def insert_element(my_list, element, pos): 
    my_list["size"] += 1 
    my_list["elements"].insert(pos, element)
    return my_list

def delete_element(my_list, pos): 
    if pos < my_list["size"] and pos >= 0:
        my_list["elements"].pop(pos)
        my_list["size"] -= 1 
    return my_list

def change_info(my_list, pos, new_info): 
    if pos < my_list["size"] and pos >= 0:
        my_list["elements"][pos] = new_info
    return my_list
    
def exchange(my_list, pos1, pos2):
    if (pos1 < my_list["size"]) and (pos2 < my_list["size"]) and (pos1 >=0) and (pos2 >=0):
        elemento = my_list["elements"][pos1]
        elemento_1 = my_list["elements"][pos2]
        my_list["elements"][pos1] = elemento_1 
        my_list["elements"][pos2] = elemento 
    return my_list

def sub_list(my_list, pos, numelem):
    sublista = {"elements": [], 
                "size": 0, 
                "type":"ARRAY_LIST"}
    b_superior = pos + numelem
    if (pos >=0) and (b_superior <= my_list["size"]): 
        sublista["elements"] = my_list["elements"][pos:b_superior]
        sublista["size"] = len(sublista["elements"]) 
    return sublista        
    

def selection_sort(my_list, sort_crit):
    """
    Implementa el algoritmo de Selection Sort para ordenar `my_list`
    según el criterio de comparación `sort_crit`.

    Args:
        my_list (list): Lista que se quiere ordenar.
        sort_crit (function): Función que recibe dos elementos de la lista y retorna True
                              si el primer elemento debe ir después del segundo, False en caso contrario.
    """
    elements = my_list['elements'] 
    n = my_list['size']

    for i in range(n):
        selected_index = i  

        for j in range(i + 1, n):

            if not sort_crit(elements[selected_index], elements[j]):
                selected_index = j

        if selected_index != i:
            elements[i], elements[selected_index] = elements[selected_index], elements[i]

    my_list['elements'] = elements
    return my_list



def merge_sort(my_list, sort_crit):
    """
    Ordena recursivamente la lista usando merge sort.
    """
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
        elements = my_list['elements']


        while i < left_size and j < right_size:
            left_element = get_element(left_half, i)
            right_element = get_element(right_half, j)
            if sort_crit(left_element, right_element):
                elements[k] = left_element
                i += 1
            else:
                elements[k] = right_element
                j += 1
            k += 1

        while i < left_size:
            elements[k] = get_element(left_half, i)
            i += 1
            k += 1

        while j < right_size:
            elements[k] = get_element(right_half, j)
            j += 1
            k += 1

    return my_list

def shell_sort(my_list, sort_crit):
    if size(my_list) > 1:
        n = size(my_list)
        h = 1
        while h < n/3:   # primer gap. La lista se h-ordena con este tamaño
            h = 3*h + 1
        while (h >= 1):
            for i in range(h, n):
                j = i
                while (j >= h) and sort_crit(
                                    get_element(my_list, j),
                                    get_element(my_list, j-h)):
                    exchange(my_list, j, j-h)
                    j -= h
            h //= 3    # h se decrementa en un tercio
    return my_list