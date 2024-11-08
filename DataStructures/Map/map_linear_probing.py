import random
from sympy import nextprime
from DataStructures.List import array_list as lt
# Implementaciones de tablas

def new_map(num_elements, load_factor, prime=109345121):
    '''
    Crea una tabla de simbolos (map) sin elementos
    Se crea una tabla de simbolos (map) sin elementos con los siguientes atributos:

    prime: Número primo utilizado en la función hash
    capacity: Tamaño de la tabla. Siguiente número primo mayor a num_elements/load_factor
    scale: Número aleatorio entre 1 y prime-1
    shift: Número aleatorio entre 0 y prime-1
    table: Lista de tamaño capacity con las entradas de la tabla
    current_factor: Factor de carga actual de la tabla, inicializado en 0
    limit_factor: Factor de carga máximo de la tabla (load_factor)
    size: Número de elementos en la tabla
    type: Tipo de tabla (PROBING)

    Parameters: num_elements (int) – Número de parejas <key,value> que inicialmente puede almacenar la tabla
    load_factor (float) – Factor de carga máximo de la tabla
    prime (int) – Número primo utilizado en la función hash. Se utiliza 109345121 por defecto

    Returns: Un nuevo map

    Return type: map_linear_probing
    '''

    capacity = nextprime(int(num_elements / load_factor))
    scale = random.randint(1, prime - 1)
    shift = random.randint(0, prime - 1)
    table = [None] * capacity

    my_map =lt.new_list()
    my_map = {
        'prime': prime,
        'capacity': capacity,
        'scale': scale,
        'shift': shift,
        'table': table,
        'current_factor': 0,
        'limit_factor': load_factor,
        'size': 0,
        'type': 'PROBING'
    }

    return my_map

def put(my_map, key, value):
    '''
    Ingresa una pareja llave,valor a la tabla de hash. Si la llave ya existe en la tabla, se reemplaza el valor

    Parameters: my_map (map_linear_probing) – El map a donde se guarda la pareja llave-valor
    key (any) – la llave asociada a la pareja
    value (any) – el valor asociado a la pareja
    Returns: El map

    Return type: map_linear_probing
    '''
    def hash_function(my_map, key):
        return (hash(key) * my_map['scale'] + my_map['shift']) % my_map['prime'] % my_map['capacity']

    # Busca la ranura donde insertar o reemplazar
    hash_value = hash_function(my_map, key)
    found, slot = find_slot(my_map, key, hash_value)

    if found:
        # Reemplaza el valor si la clave ya existe
        my_map['table'][slot] = (key, value)
    else:
        # Si no se encuentra la clave, inserta y verifica si se necesita rehash
        my_map['table'][slot] = (key, value)
        my_map['size'] += 1
        my_map['current_factor'] = my_map['size'] / my_map['capacity']

        # Rehash si el factor de carga supera el límite
        if my_map['current_factor'] >= my_map['limit_factor']:
            my_map = rehash(my_map)
    
    return my_map

def contains(my_map, key):
    '''
    Valida si la llave key se encuentra en el map
    Retorna True si la llave key se encuentra en el my_map o False en caso contrario.

    Parameters: my_map (map_linear_probing) – El my_map a donde se guarda la pareja
    key (any) – la llave asociada a la pareja
    Returns: True si la llave se encuentra en el map, False en caso contrario
    Return type: bool
    '''
    hash_value = (hash(key) * my_map['scale'] + my_map['shift']) % my_map['prime'] % my_map['capacity']
    found, _ = find_slot(my_map, key, hash_value)
    return found

def get(my_map, key):
    '''
    Retorna el valor asociado a la llave key en el map

    Parameters: my_map (map_linear_probing) – Map a examinar
    key (any) – Llave a buscar
    Returns: Valor asociado a la llave key

    Return type: any
    '''
    hash_value = (hash(key) * my_map['scale'] + my_map['shift']) % my_map['prime'] % my_map['capacity']
    found, slot = find_slot(my_map, key, hash_value)
    
    if found:
        return my_map['table'][slot][1]
    else:
        return None

def remove(my_map, key):
    '''
    Elimina la pareja llave-valor del map

    Parameters: my_map (map_linear_probing) – El map a examinar
    key (any) – Llave a eliminar
    Returns: El map sin la llave key

    Return type: map_linear_probing
    '''
    hash_value = (hash(key) * my_map['scale'] + my_map['shift']) % my_map['prime'] % my_map['capacity']
    found, slot = find_slot(my_map, key, hash_value)
    
    if found:
        my_map['table'][slot] = ('_EMPTY', 'EMPTY_')
        my_map['size'] -= 1
        my_map['current_factor'] = my_map['size'] / my_map['capacity']
    else:
        raise Exception('Key not found')

    return my_map

def size(my_map):
    '''
    Retorna el número de parejas llave-valor en el map

    Parameters: my_map (map_linear_probing) – El map a examinar
    Returns: Número de parejas llave-valor en el map

    Return type: int
    '''
    return my_map['size']

def is_empty(my_map):
    '''
    Indica si el map se encuentra vacío

    Parameters: my_map (map_linear_probing) – El map a examinar
    Returns: True si el map está vacío, False en caso contrario

    Return type: bool
    '''
    
    if my_map['size'] == 0:
        return True
    else:
        return False

def key_set(my_map):
    '''
    Retorna una lista con todas las llaves de la tabla de hash

    Parameters: my_map (map_linear_probing) – El map a examinar
    Returns: lista de llaves
    Return type: array_list
    '''
    keys = lt.new_list()
    for entry in my_map['table']:
        if entry is not None and entry != ('_EMPTY', 'EMPTY_'):
            lt.add_last(keys, entry[0])
    return keys



def value_set(my_map):
    '''
    Retorna una lista con todos los valores de la tabla de hash

    Parameters: my_map (map_linear_probing) – El map a examinar
    Returns: lista de valores

    Return type: array_list
    '''
    
    values = lt.new_list()
    for entry in my_map['table']:
        if entry is not None and entry != ('_EMPTY', 'EMPTY_'):
            lt.add_last(values, entry[1])
    return values

def find_slot(my_map, key, hash_value):
    '''
    Busca la key a partir de una posición dada en la tabla.
    Utiliza la función de hash para encontrar la posición inicial de la llave. Si la posición está ocupada, busca la siguiente posición disponible.
    Usa la función de comparación (default_compare) para determinar si la llave ya existe en la tabla.

    Parameters: my_map (map_linear_probing) – El map a examinar
    key (any) – Llave a buscar
    hash_value (int) – Posición inicial de la llave

    Returns: Retorna una tupla con dos valores. El primero indica si la posición está ocupada, True si se encuentra la key de lo contrario False. El segundo la posición en la tabla de hash donde se encuentra o posición libre para agregarla

    Return type: bool, int
    '''
    pos = hash_value
    capacity = my_map['capacity']
    first_empty = None  # Almacena la primera posición '_EMPTY_'

    while my_map['table'][pos] is not None:
        k, _ = my_map['table'][pos]

        # Si encontramos la clave, devolvemos la posición
        if k == key:
            return True, pos

        # Marca la primera posición vacía o eliminada
        if first_empty is None and k == '_EMPTY_':
            first_empty = pos

        # Avanza al siguiente índice (sondeo lineal)
        pos = (pos + 1) % capacity
    
    # Si encontramos un espacio '_EMPTY_', lo usamos como posición para nuevas inserciones
    if first_empty is not None:
        return False, first_empty

    # Retorna la primera posición realmente vacía
    return False, pos

def is_available(table, pos):
    '''
    Informa si la posición pos está disponible en la tabla de hash.
    Se entiende que una posición está disponible si su contenido es igual a None (no se ha usado esa posición) o a _EMPTY_ (la posición fue liberada)

    Parameters: table (array_list) – Tabla de hash, implementada como una lista (array_list)
    pos (int) – Posición a verificar

    Returns: True si la posición está disponible, False en caso contrario

    Return type: bool
    '''
    if table[pos] is None or table[pos] == ('_EMPTY', 'EMPTY_'):
        return True
    else:
        return False

def rehash(my_map):
    '''
    Hace rehash de todos los elementos de la tabla de hash.
    Incrementa la capacidad de la tabla al doble y se hace rehash de todos los elementos de la tabla uno por uno.
    Se utiliza la función hash_value para calcular el nuevo hash de cada llave.
    
    Parameters: my_map (map_linear_probing) – El map a hacer rehash
    Returns: El map con la nueva capacidad
    Return type: map_linear_probing
    '''
    old_table = my_map['table']
    new_capacity = nextprime(2 * my_map['capacity'])
    my_map['table'] = [None] * new_capacity
    my_map['capacity'] = new_capacity
    my_map['size'] = 0
    my_map['current_factor'] = 0

    for entry in old_table:
        if entry is not None:
            key, value = entry
            put(my_map, key, value)
    
    return my_map

def default_compare(key, element):
    '''Función de comparación por defecto. Compara una llave con la llave de un elemento llave-valor.

    Parameters:
    key (any) – Llave a comparar
    element (map_entry) – entry a comparar
    Returns: 0 si son iguales, 1 si key > la llave del element, -1 si key < que la llave del element

    Return type: int
    '''
    if key == element:
        return 0
    elif key > element:
        return 1
    else:
        return -1