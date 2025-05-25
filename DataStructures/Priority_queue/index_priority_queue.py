from DataStructures.Map import map_linear_probing as map
from DataStructures.List import array_list as lt


def new_index_heap(is_min_pq=True):
    """
    Crea un cola de prioridad indexada orientada a menor o mayor dependiendo del valor de ``is_min_pq``

    Se crea una cola de prioridad con los siguientes atributos:

    - **elements**: Lista de elementos. Se inicializa como una lista vacia.
    - **qp_map**: Mapa de llave a indice. Se inicializa como un mapa vacio con un ``num_elements`` de 100 inicial.
    - **size**: El numero de elementos. Se inicializa en 0.
    - **cmp_function**: La funcion de comparacion. Si es una cola de prioridad orientada a menor ``is_min_pq = True``, se inicializa con la funcion ``cmp_function_lower_value``. Si es una cola de prioridad orientada a mayor ``is_min_pq = False``, se inicializa con la funcion ``cmp_function_higher_value``.

    :param is_min_pq: Indica si la cola de prioridad es orientada a menor o mayor. Por defecto es ``True``.
    :type is_min_pq: bool

    :return: Una nueva cola de prioridad indexada
    :rtype: index_priority_queue
    """
    indexheap = {
        "elements": None,
        "qp_map": None,
        "size": 0,
        "cmp_function": None,
    }
    if is_min_pq:
        indexheap["cmp_function"] = cmp_function_lower_value
    else:
        indexheap["cmp_function"] = cmp_function_higher_value
    indexheap["elements"] = lt.new_list()
    lt.add_last(indexheap["elements"], None)
    indexheap["qp_map"] = map.new_map(num_elements=100, load_factor=0.5)
    return indexheap


def cmp_function_higher_value(father_node, child_node):
    """
    Valida si el nodo padre tiene mayor prioridad que el nodo hijo

    :param father_node: El nodo padre
    :type father_node: dict
    :param child_node: El nodo hijo
    :type child_node: dict

    :return: ``True`` si el nodo padre tiene mayor prioridad que el nodo hijo. ``False`` en caso contrario.
    :rtype: bool
    """
    if father_node["index"] >= child_node["index"]:
        return True
    return False


def cmp_function_lower_value(father_node, child_node):
    """
    Valida si el nodo padre tiene menor prioridad que el nodo hijo

    :param father_node: El nodo padre
    :type father_node: dict
    :param child_node: El nodo hijo
    :type child_node: dict

    :return: ``True`` si el nodo padre tiene menor prioridad que el nodo hijo. ``False`` en caso contrario.
    :rtype: bool
    """
    if father_node["index"] <= child_node["index"]:
        return True
    return False


def insert(my_heap, index, key):
    """
    Inserta la llave ``key`` con prioridad ``index`` en el heap.

    :param my_heap: El heap indexado
    :type my_heap: index_priority_queue
    :param index: La prioridad de la llave
    :type index: int
    :param key: La llave a insertar
    :type key: any

    :return: El heap con la nueva paraja indexada
    :rtype: index_priority_queue
    """
    if not map.contains(my_heap["qp_map"], key):
        my_heap["size"] += 1
        lt.insert_element(
            my_heap["elements"], {"key": key, "index": index}, my_heap["size"]
        )
        map.put(my_heap["qp_map"], key, my_heap["size"])
        swim(my_heap, my_heap["size"])
    return my_heap


def is_empty(my_heap):
    """
    Informa si una cola de prioridad indexada es vacia.

    :param my_heap: El heap indexado a revisar
    :type my_heap: index_priority_queue

    :return: ``True`` si esta vacia. ``False`` en caso contrario.
    :rtype: bool
    """
    return my_heap["size"] == 0


def size(my_heap):
    """
    Retorna el número de elementos en el heap.

    :param my_heap: El heap a revisar
    :type my_heap: index_priority_queue

    :return: El número de elementos
    :rtype: int
    """
    return my_heap["size"]


def contains(my_heap, key):
    """
    Indica si la llave key se encuentra en el heap.

    :param my_heap: El heap a revisar
    :type my_heap: index_priority_queue
    :param key: La llave a buscar
    :type key: any

    :return: ``True`` si la llave se encuentra en el heap. ``False`` en caso contrario.
    :rtype: bool
    """
    return map.contains(my_heap["qp_map"], key)


def get_first_priority(my_heap):
    """
    Retorna el primer elemento del heap, es decir el elemento con mayor prioridad sin eliminarlo.

    .. important:: Si el heap es orientado a menor, el primer elemento es el de menor valor. Si el heap es orientado a mayor,
    el primer elemento es el de mayor valor.

    :param my_heap: El heap a revisar
    :type my_heap: index_priority_queue

    :return: La llave asociada al mayor indice
    :rtype: any
    """
    if my_heap["size"] > 0:
        max_idx = lt.get_element(my_heap["elements"], 1)
        return max_idx["key"]
    return None


def remove(my_heap):
    """
    Retorna el elemento del heap de mayor prioridad y lo elimina.
    Se reemplaza con el último elemento y se hace **sink**.

    .. important:: Si el heap es orientado a menor, el primer elemento es el de menor valor.
        Si el heap es orientado a mayor, el primer elemento es el de mayor valor.

    :param my_heap: El heap a revisar
    :type my_heap: index_priority_queue

    :return: La llave asociada al indice con mayor prioridad
    :rtype: any
    """
    if my_heap["size"] > 0:
        min_idx = lt.get_element(my_heap["elements"], 1)
        exchange(my_heap, 1, my_heap["size"])
        my_heap["size"] -= 1
        lt.remove_last(my_heap["elements"])
        sink(my_heap, 1)
        map.remove(my_heap["qp_map"], min_idx["key"])
        return min_idx["key"]
    return None


def decrease_key(my_heap, key, new_index):
    """
    Decrementa el indice de un llave

    :param my_heap: El heap a revisar
    :type my_heap: index_priority_queue
    :param key: la llave a decrementar
    :type key: any
    :param new_index: El nuevo indice de la llave
    :type new_index: int

    :return: El heap con la llave decrementada
    :rtype: index_priority_queue
    """
    val = map.get(my_heap["qp_map"], key)
    elem = lt.get_element(my_heap["elements"], val)
    elem["index"] = new_index
    lt.change_info(my_heap["elements"], val, elem)
    swim(my_heap, val)
    return my_heap


def increase_key(my_heap, key, new_index):
    """
    Incrementa el indice de un llave

    :param my_heap: El heap a revisar
    :type my_heap: index_priority_queue
    :param key: la llave a incrementar
    :type key: any
    :param new_index: El nuevo indice de la llave
    :type new_index: int

    :return: El heap con la llave incrementada
    :rtype: index_priority_queue
    """
    val = map.get(my_heap["qp_map"], key)
    elem = lt.get_element(my_heap["elements"], val)
    elem["index"] = new_index
    lt.change_info(my_heap["elements"], val, elem)
    sink(my_heap, val)
    return my_heap


#  ---------------------------------------------------------
#   Funciones Helper
#  ---------------------------------------------------------

"""
""" """""" """""" """""" """""
Las siguientes funciones son funciones auxiliares para el manejo de un heap indexado.
""" """""" """""" """""" """""
"""


def exchange(my_heap, pos_i, pos_j):
    """
    Intercambia los elementos en las posiciones ``pos_i`` y ``pos_j`` del heap

    :param my_heap: El heap a revisar
    :type my_heap: index_priority_queue
    :param pos_i: La posición del primer elemento
    :type pos_i: int
    :param pos_j: La posición del segundo elemento
    :type pos_j: int
    """
    element_i = lt.get_element(my_heap["elements"], pos_i)
    element_j = lt.get_element(my_heap["elements"], pos_j)
    lt.change_info(my_heap["elements"], pos_i, element_j)
    map.put(my_heap["qp_map"], element_i["key"], pos_j)
    lt.change_info(my_heap["elements"], pos_j, element_i)
    map.put(my_heap["qp_map"], element_j["key"], pos_i)


def priority(my_heap, parent, child):
    """
    Indica si el ``parent`` tiene mayor prioridad que ``child``.

    .. important:: La prioridad se define por la función de comparación del heap. Si es un heap orientado a menor,
        la prioridad es menor si el ``parent`` es menor que el ``child``. Si es un heap orientado a mayor, la prioridad es mayor
        si el ``parent`` es mayor que el ``child``.

    :param my_heap: El heap a revisar
    :type my_heap: index_priority_queue
    :param parent: El elemento padre
    :type parent: any
    :param child: El elemento hijo a comparar
    :type child: any

    :returns: ``True`` si el ``parent`` tiene mayor prioridad que el ``child``. ``False`` en caso contrario.
    :rtype: bool
    """
    compare_function = my_heap["cmp_function"]
    return compare_function(parent, child)


def swim(my_heap, pos):
    """
    Deja en el lugar indicado un elemento adicionado en la última posición

    :param my_heap: El heap sobre el cual se realiza la operación
    :type my_heap: index_priority_queue
    :param pos: La posición del elemento a revisar
    :type pos: int
    """
    find = False
    while pos > 1 and not find:
        posparent = int((pos // 2))
        poselement = int(pos)
        parent = lt.get_element(my_heap["elements"], posparent)
        element = lt.get_element(my_heap["elements"], poselement)
        if not priority(my_heap, parent, element):
            exchange(my_heap, posparent, poselement)
        else:
            find = True
        pos = pos // 2


def sink(my_heap, pos):
    """
    Deja en la posición correcta un elemento ubicado en la raíz del heap

    :param my_heap: El heap sobre el cual se realiza la operación
    :type my_heap: index_priority_queue
    :param pos: La posición del elemento a revisar
    :type pos: int
    """
    size = my_heap["size"]
    while 2 * pos <= size:
        j = 2 * pos
        if j < size:
            if not priority(
                my_heap,
                lt.get_element(my_heap["elements"], j),
                lt.get_element(my_heap["elements"], (j + 1)),
            ):
                j += 1
        if priority(
            my_heap,
            lt.get_element(my_heap["elements"], pos),
            lt.get_element(my_heap["elements"], j),
        ):
            break
        exchange(my_heap, pos, j)
        pos = j