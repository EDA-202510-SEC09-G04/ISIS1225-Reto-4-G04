from DataStructures.List import single_linked_list as lt
from DataStructures.Utils import error as error

"""
  Este módulo implementa el tipo abstracto de datos pila
  (Stack) sobre una lista encadenada.
"""


def new_stack():
    """Crea una pila vacia.

    Implementa una pila sobre una alguna de las implementaciones de listas

    :returns: Una pila vacia
    :rtype: stack
    """
    try:
        return lt.new_list()
    except Exception as exp:
        error.reraise(exp, "TADStack->new_stack: ")


def push(my_stack, element):
    """Agrega el elemento ``element`` en el tope de la pila.

    :param my_stack: La pila donde se insetará el elemento
    :type my_stack: stack
    :param element: El elemento a insertar
    :type element: any

    :returns: La pila modificada
    :rtype: stack
    """
    try:
        lt.add_last(my_stack, element)
        return my_stack
    except Exception as exp:
        error.reraise(exp, "TADmy_Stack->Push: ")


def pop(my_stack):
    """Retorna y elimina el elemento presente en el tope de la pila.

    Si la pila está vacía, retorna ``None``.

    :param my_stack: La pila de donde se retirara el elemento
    :type my_stack: stack

    :returns: El elemento del tope de la pila
    :rtype: any
    """
    try:
        if my_stack is not None and not lt.is_empty(my_stack):
            return lt.remove_last(my_stack)
        else:
            raise Exception
    except Exception as exp:
        error.reraise(exp, "TADStack->pop: ")


def is_empty(my_stack):
    """Informa si la pila es vacía.

    :param my_stack: La pila a examinar
    :type my_stack: stack

    :returns: ``True`` si la pila es vacia, ``False`` de lo contrario
    :rtype: bool
    """
    try:
        return lt.is_empty(my_stack)
    except Exception as exp:
        error.reraise(exp, "TADStack->is_empty: ")


def top(my_stack):
    """Retorna el elemento en tope de la pila, sin eliminarlo de la pila.

    :param my_stack: La pila a examinar
    :type my_stack: stack

    :returns: El elemento en el tope de la pila
    :rtype: any
    """
    try:
        return lt.last_element(my_stack)
    except Exception as exp:
        error.reraise(exp, "TADStack->top: ")


def size(my_stack):
    """Informa el número de elementos en la pila.

    :param my_stack: La pila a examinar
    :type my_stack: stack

    :returns: El número de elementos en la pila
    :rtype: int
    """
    try:
        return lt.size(my_stack)
    except Exception as exp:
        error.reraise(exp, "TADStack->size: ")