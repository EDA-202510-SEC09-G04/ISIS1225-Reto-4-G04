def new_list():
    newlist = {
        'elements': [],
        'size': 0,
    }
    return newlist


def get_element(my_list, pos):
    if pos < 0 or pos > size(my_list):
        raise Exception('IndexError: list index out of range')
    return my_list['elements'][pos]

def is_present(my_list,element, cmp_function):
    size = len(my_list['elements'])
    if size > 0:
        keyexist = False
        for keypos in range(0,size):
            info = my_list["elements"][keypos]
            if cmp_function(element, info) == 0 :
                keyexist = True
                break
        if  keyexist:
            return keypos
    return -1


def size(my_list):
    value = my_list['size']
    return value

def add_first(my_list,element):
    if len(my_list['elements']) == 0:
        my_list['elements'] = [None]
        
    if my_list['size'] >= len(my_list['elements']):
        capacidad = 2 * len(my_list['elements'])
        elements = [None] * capacidad
        for i in range(my_list['size']):
            elements[i + 1] = my_list['elements'][i]
        my_list['elements'] = elements
    else:
        for i in range(my_list['size'], 0, -1):
            my_list['elements'][i] = my_list['elements'][i - 1]
    my_list['elements'][0] = element
    my_list['size'] += 1

    return my_list

""" def add_last(my_list,element):
    if my_list['size'] == 0:
        my_list['elements'] = [None] * 1
    
    if my_list['size'] == len(my_list['elements']):  
        new_size = max(1, my_list['size'] * 2)  
        new_elements = [None] * new_size  
        
        for i in range(my_list['size']):
            new_elements[i] = my_list['elements'][i]
        
        my_list['elements'] = new_elements  

    my_list['elements'][my_list['size']] = element 
    my_list['size'] += 1 
    
    return my_list """

def add_last(my_list, element):
    if 'elements' not in my_list:
        my_list['elements'] = []
        my_list['size'] = 0
    
    my_list['elements'].append(element)
    my_list['size'] += 1

def first_element(my_list):
    if size(my_list) == 0:
        raise Exception('IndexError: list index out of range')
    return my_list['elements'][0]

def last_element(my_list):
    if size(my_list) == 0:
        raise Exception('IndexError: list index out of range')
    return my_list[size(my_list)-1]

def get_element(my_list,pos):
    if pos < 0 or pos > size(my_list):
        raise Exception('IndexError: list index out of range')
    return my_list['elements'][pos]

def delete_element(my_list,pos):
    if pos < 0 or pos > size(my_list):
        raise Exception('IndexError: list index out of range')
    elemento = my_list['elements'][pos]
    for i in range(pos, my_list['size'] - 1):
        my_list['elements'][i] = my_list['elements'][i + 1]
    
    my_list['elements'][my_list['size'] - 1] = None
    my_list['size'] -= 1
    return my_list

def remove_first(my_list):
    if size(my_list) == 0:
        raise Exception('IndexError: list index out of range')
    elemento = my_list['elements'][0]
    for i in range(1, my_list['size']):
        my_list['elements'][i-1] = my_list['elements'][i]
    
    my_list['elements'][my_list['size'] - 1] = None
    my_list['size'] -= 1
    return elemento
    
def remove_last(my_list):
    if size(my_list) == 0:
        raise Exception('IndexError: list index out of range')
    
    elemento = my_list['elements'][my_list['size']-1]
    my_list['elements'][my_list['size']-1] = None
    my_list['size'] -= 1
    return elemento

def insert_element(my_list, element, pos):
    if 0 <= pos <= len(my_list):
        my_list.insert(pos, element)
    else:
        raise IndexError('list index out of range')

    my_list['size'] += 1
    return my_list

def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= my_list['size'] or my_list['size'] == 0:
        raise IndexError('list index out of range')
    my_list['elements'][pos] = new_info
    return my_list

def exchange(my_list, pos_1, pos_2):
    if (pos_1 < 0 or pos_1 >= my_list['size'] or
        pos_2 < 0 or pos_2 >= my_list['size']):
        raise Exception('list index out of range')
    primero = pos_1
    segundo = pos_2
    my_list['elements'][pos_1] = segundo
    my_list['elements'][pos_2] = primero
    return my_list

def sub_list(my_list, pos_i, num_elements):
    if pos_i < 0 or pos_i >= my_list['size']:
        raise IndexError('list index out of range')
    if pos_i + num_elements > my_list['size']:
        raise IndexError('list index out of range')
    
    sublist = {
        'elements': my_list['elements'][pos_i:pos_i + num_elements],
        'size': num_elements
    }
    return sublist

def is_empty(my_list):
    if my_list["size"] == 0 or my_list["size"] == None:
        return True
    else:
        return False
    



    
