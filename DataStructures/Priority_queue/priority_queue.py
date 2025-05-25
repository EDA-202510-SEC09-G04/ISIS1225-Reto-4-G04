from DataStructures.List import array_list as lt


def new_heap(is_min_pq=True):
    """
    Crea un cola de prioridad indexada orientada a menor o mayor dependiendo del valor de ``is_min_pq``

    Se crea una cola de prioridad con los siguientes atributos:

    - **elements**: Lista de elementos. Se inicializa como una lista vacia.
    - **cmp_function**: La funcion de comparacion. Si es una cola de prioridad orientada a menor ``is_min_pq = True``, se inicializa con la funcion ``cmp_function_lower_value``. Si es una cola de prioridad orientada a mayor ``is_min_pq = False``, se inicializa con la funcion ``cmp_function_higher_value``.

    :param is_min_pq: Indica si la cola de prioridad es orientada a menor o mayor. Por defecto es ``True``.
    :type is_min_pq: bool

    :return: Una nueva cola de prioridad indexada
    :rtype: priority_queue
    """
    heap = {"elements": lt.new_list(), "size": 0, "cmp_function": None}
    lt.add_last(heap["elements"], None)
    if is_min_pq:
        heap["cmp_function"] = cmp_function_lower_value
    else:
        heap["cmp_function"] = cmp_function_higher_value
    return heap


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
    if father_node["key"] >= child_node["key"]:
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
    if father_node["key"] <= child_node["key"]:
        return True
    return False


def size(my_heap):
    """
    Retorna el número de elementos en el heap.

    :param my_heap: El heap a revisar
    :type my_heap: priority_queue

    :return: El número de elementos
    :rtype: int
    """
    return my_heap["size"]


def is_empty(my_heap):
    """
    Informa si una cola de prioridad es vacia.

    :param my_heap: El heap indexado a revisar
    :type my_heap: priority_queue

    :return: ``True`` si esta vacia. ``False`` en caso contrario.
    :rtype: bool
    """
    return my_heap["size"] == 0


def get_first_priority(my_heap):
    """
    Retorna el primer elemento del heap, es decir el elemento con mayor prioridad sin eliminarlo.

    .. important:: Si el heap es orientado a menor, el primer elemento es el de menor valor. Si el heap es orientado a mayor,
    el primer elemento es el de mayor valor.

    :param my_heap: El heap a revisar
    :type my_heap: priority_queue

    :return: El valor asociada al mayor indice
    :rtype: any
    """
    if my_heap["size"] > 0:
        return lt.get_element(my_heap["elements"], 1)["value"]
    return None


def insert(my_heap, element, key):
    """
    Inserta la llave ``key`` con prioridad ``value`` en el heap.

    :param my_heap: El heap indexado
    :type my_heap: priority_queue
    :param element: El valor de la llave
    :type element: int
    :param key: La llave a insertar
    :type key: any

    :return: El heap con la nueva paraja insertada
    :rtype: priority_queue
    """
    my_heap["size"] += 1
    lt.insert_element(my_heap["elements"], {
                      "key": key, "value": element}, my_heap["size"])
    swim(my_heap, my_heap["size"])
    return my_heap


def remove(my_heap):
    """
    Retorna el elemento del heap de mayor prioridad y lo elimina.
    Se reemplaza con el último elemento y se hace **sink**.

    .. important:: Si el heap es orientado a menor, el primer elemento es el de menor valor.
        Si el heap es orientado a mayor, el primer elemento es el de mayor valor.

    :param my_heap: El heap a revisar
    :type my_heap: priority_queue

    :return: Valor asociado a la key con mayor prioridad
    :rtype: any
    """
    if my_heap["size"] > 0:
        min = lt.get_element(my_heap["elements"], 1)
        last = lt.get_element(my_heap["elements"], my_heap["size"])
        lt.change_info(my_heap["elements"], 1, last)
        lt.remove_last(my_heap["elements"])
        my_heap["size"] -= 1
        sink(my_heap, 1)
        return min["value"]
    return None


# _____________________________________________________________________________
#       Funciones Helper
# _____________________________________________________________________________


def swim(my_heap, pos):
    """
    Deja en el lugar indicado un elemento adicionado en la última posición

    :param my_heap: El heap sobre el cual se realiza la operación
    :type my_heap: priority_queue
    :param pos: La posición del elemento a revisar
    :type pos: int
    """
    found = False
    while pos > 1 and not found:
        parent = lt.get_element(my_heap["elements"], int((pos // 2)))
        element = lt.get_element(my_heap["elements"], int(pos))
        if not priority(my_heap, parent, element):
            exchange(my_heap, pos, int(pos / 2))
        else:
            found = True
        pos = pos // 2


def sink(my_heap, pos):
    """
    Deja en la posición correcta un elemento ubicado en la raíz del heap

    :param my_heap: El heap sobre el cual se realiza la operación
    :type my_heap: priority_queue
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


def priority(my_heap, parent, child):
    """
    Indica si el ``parent`` tiene mayor prioridad que ``child``.

    .. important:: La prioridad se define por la función de comparación del heap. Si es un heap orientado a menor,
        la prioridad es menor si el ``parent`` es menor que el ``child``. Si es un heap orientado a mayor, la prioridad es mayor
        si el ``parent`` es mayor que el ``child``.

    :param my_heap: El heap a revisar
    :type my_heap: priority_queue
    :param parent: El elemento padre
    :type parent: any
    :param child: El elemento hijo a comparar
    :type child: any

    :returns: ``True`` si el ``parent`` tiene mayor prioridad que el ``child``. ``False`` en caso contrario.
    :rtype: bool
    """
    cmp = my_heap["cmp_function"](parent, child)
    if cmp > 0:
        return True
    return False


def exchange(my_heap, pos_i, pos_j):
    """
    Intercambia los elementos en las posiciones ``pos_i`` y ``pos_j`` del heap

    :param my_heap: El heap a revisar
    :type my_heap: priority_queue
    :param pos_i: La posición del primer elemento
    :type pos_i: int
    :param pos_j: La posición del segundo elemento
    :type pos_j: int
    """
    lt.exchange(my_heap["elements"], pos_i, pos_j)