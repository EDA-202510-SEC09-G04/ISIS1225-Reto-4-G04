from DataStructures.List import array_list as lt
from DataStructures.Utils import error as error

"""
  Este módulo implementa el tipo abstracto de datos
  cola (Queue) sobre una lista.
"""


def new_queue():
    """ Crea una cola vacia basada en una array list.

        Implementa una cola sobre una alguna de las implementaciones de listas

        :returns: Una cola vacia
        :rtype: queue
    """
    try:
        return lt.new_list()
    except Exception as exp:
        error.reraise(exp, 'TADQueue->new_queue: ')


def enqueue(my_queue, element):
    """ Agrega el elemento ``element`` el final de la cola.

        :param my_queue: La cola donde se insertará el elemento
        :type my_queue: queue
        :param element: El elemento a insertar
        :type element: any

        :returns: La cola modificada
        :rtype: queue
    """
    try:
        lt.add_last(my_queue, element)
        return my_queue
    except Exception as ex:
        error.reraise(ex, 'enqueue ')


def dequeue(my_queue):
    """ Retorna el elemento en la primer posición de la cola, y lo elimina.

        :param my_queue: La cola de donde se retirara el elemento
        :type my_queue: queue

        :returns: El primer elemento de la cola
        :rtype: any
    """
    try:
        return lt.remove_first(my_queue)
    except Exception as exp:
        error.reraise(exp, 'TADmy_Queue->demy_queue: ')


def peek(my_queue):
    """ Retorna el elemento en la primer posición de la cola sin eliminarlo.

        :param my_queue: La cola a examinar
        :type my_queue: queue

        :returns: El primer elemento de la cola
        :rtype: any
    """
    try:
        return lt.first_element(my_queue)
    except Exception as exp:
        error.reraise(exp, 'TADQueue->is_empty: ')


def is_empty(my_queue):
    """ Informa si la cola es vacía.

        :param my_queue: La cola a examinar
        :type my_queue: queue

        :returns: ``True`` si la cola es vacia, ``False`` de lo contrario
        :rtype: bool
    """
    try:
        return lt.is_empty(my_queue)
    except Exception as exp:
        error.reraise(exp, 'TADQueue->is_empty: ')


def size(my_queue):
    """ Informa el número de elementos en la cola

        :param my_queue: La cola a examinar
        :type my_queue: queue

        :returns: El número de elementos en la cola
        :rtype: int
    """
    try:
        return lt.size(my_queue)
    except Exception as exp:
        error.reraise(exp, 'TADQueue->size: ')