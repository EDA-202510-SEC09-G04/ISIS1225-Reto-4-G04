from DataStructures.List import array_list as lt

def new_queue():
    my_queue = {"elements": [],
                "size": 0}
    
    return my_queue

# Listo perfecto quedo bien implementada. print(new_queue())


def enqueue(my_queue, element):
    lt.add_last(my_queue,element)
    return my_queue


def dequeue(my_queue):
    if my_queue['size'] == 0:
        raise Exception('EmptyStructureError: queue is empty')
    else:
        a =lt.remove_first(my_queue)
    return a


def peek(my_queue):
    if my_queue['size'] == 0:
        raise Exception('EmptyStructureError: queue is empty')
    else:
        return my_queue['elements'][0]

def is_empty(my_queue):
    vacia = False
    if my_queue['size'] == 0:
        vacia = True
    return vacia

def size(my_queue):
    return my_queue['size']

