def new_list():
    newlist ={
        'first': None,
        'last': None,
        'size': 0,
    }
    return newlist


def get_element(my_list, pos):
    if pos < 0 or pos >= size(my_list): 
        raise IndexError('list index out of range')  
    
    node = my_list["first"]
    searchpos = 0
    
    while searchpos < pos:
        if node is None:
            raise IndexError('list index out of range')
        node = node["next"]
        searchpos += 1

    if node is None:
        raise IndexError('list index out of range')

    return node["info"]



def is_present(my_list,element, cmp_function): 
    is_in_array = False
    temp = my_list['first']
    count = 0
    while not is_in_array and temp is not None:
        if cmp_function(element, temp['info']) == 0:
            is_in_array = True
        else:
            temp = temp['next']
            count += 1
            
    if not is_in_array:
        count = -1
    return count
    
    
def size(my_list):
    return my_list['size']


def add_first(my_list, element):
    dict_element = {
        'info': element,
        'next': my_list['first'] 
    }

    my_list['first'] = dict_element 
    
    if my_list['last'] is None: 
        my_list['last'] = dict_element

    my_list['size'] += 1
    
    return my_list




def add_last(my_list,element):
    
    dict_element = {}
    dict_element['info'] = element
    dict_element['next'] = None
    
    if my_list['last'] == None:
        my_list['first'] = dict_element
        my_list['last'] = dict_element
    else:
        my_list['last']['next'] = dict_element
        my_list['last'] = dict_element
        
    my_list['size'] += 1
    return my_list

def first_element(my_list):
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
    return my_list['first']
    
def last_element(my_list):
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
    return my_list['last']
    
    
def is_empty(my_list):
    if my_list['size'] == 0:
        return True
    else:
        return False
    
def remove_first(my_list):
    if size(my_list) == 0:
        raise IndexError('list index out of range')
    
    node = my_list['first']
            
    if my_list['first']['next'] is None:
        my_list['first'] = None
        my_list['last'] = None
    else:
        my_list['first'] = my_list['first']['next']
        
    my_list['size'] -= 1
    return node['info']
        
        
def remove_last(my_list):
    if my_list['first'] is None:
        raise IndexError('list index out of range')
    
    temp = my_list['first']
    
    if temp['next'] is None:
        return remove_first(my_list)
    
    while temp['next']['next'] is not None:
        temp = temp['next']
        
    node = temp['next']
    temp['next'] = None
    my_list['last'] = temp
    my_list['size'] -= 1

    return node['info']

  
    
def insert_element(my_list,element,pos):
    if pos < 0 or pos > size(my_list):
        raise Exception('IndexError: list index out of range')
    
    new_node = {
        'info': element,
        'next': None
    }
    if pos == 0:
        return add_first(my_list,element)
    elif pos == size(my_list):
        return add_last(my_list,element)
    else:
        temp = my_list['first']
        for i in range(pos - 1):
            temp = temp['next']

        new_node['next'] = temp['next']
        temp['next'] = new_node
        
    my_list['size'] += 1
    return my_list
    
def delete_element(my_list,pos):
    if pos < 0 or pos >= size(my_list):
        raise Exception('IndexError: list index out of range')
  
    if pos == 0:
        remove_first(my_list)
        return my_list
    elif pos == size(my_list) -1:
        remove_last(my_list)
        return my_list
    else:
        
        temp = my_list['first']
        for i in range(pos - 1):
            temp = temp['next']

        node = temp['next']
        temp['next'] = node['next']
        
    my_list['size'] -= 1
    return my_list

def change_info(my_list, pos, new_info):
    if pos < 0 or pos >= size(my_list):
        raise Exception('IndexError: list index out of range')
    
    node = my_list["first"]
    for i in range(pos):
        node = node["next"]

    node["info"] = new_info 
    return my_list

def exchange(my_list, pos_1, pos_2):
    if pos_1 == pos_2:
        return my_list

    info1 = get_element(my_list, pos_1)
    info2 = get_element(my_list, pos_2)

    change_info(my_list, pos_1, info2)
    change_info(my_list, pos_2, info1)

    return my_list


    

def sub_list(my_list, pos_i, num_elements):
    if pos_i < 0 or pos_i >= size(my_list):
        raise Exception('IndexError: list index out of range')
    if pos_i + num_elements > size(my_list):
        raise Exception('IndexError: list index out of range')
    
    node_1 = get_element(my_list,pos_i)

    sublist ={
        'first': node_1,
        'last': None,
        'size': num_elements,
    }
    
    node_2 = get_element(my_list,num_elements)
    sublist['last'] = node_2
        
    return sublist
def partition(my_list, lo, hi, sort_crit):
    pivot = get_element(my_list, hi)
    i = lo

    for j in range(lo, hi):
        if sort_crit(get_element(my_list, j), pivot):
            exchange(my_list, i, j)
            i += 1

    exchange(my_list, i, hi)
    return i

def shell_sort(my_list, sort_crit):
    if size(my_list) > 1:
        n = size(my_list)
        h = 1
        while h < n/2:  
            h = 2*h + 1
        while (h >= 1):
            for i in range(h, n):
                j = i
                while (j >= h) and sort_crit(
                                    get_element(my_list, j),
                                    get_element(my_list, j-h)):
                    exchange(my_list, j, j-h)
                    j -= h
            h //= 2   
    return my_list

def insertion_sort(my_list, sort_crit):

    if size(my_list) > 1:
        n = size(my_list)
        pos1 = 0
        while pos1 < n:
            pos2 = pos1
            while (pos2 > 0) and (sort_crit(
                get_element(my_list, pos2), get_element(my_list, pos2-1))):
                exchange(my_list, pos2, pos2-1)
                pos2 -= 1
            pos1 += 1
    return my_list

def quick_sort(my_list, sort_crit):

    quick_sort_recursive(my_list, 0, size(my_list)-1, sort_crit)
    return my_list

def quick_sort_recursive(my_list, lo, hi, sort_crit):
 
    if (lo >= hi):
        return
    pivot = partition(my_list, lo, hi, sort_crit)
    quick_sort_recursive(my_list, lo, pivot-1, sort_crit)
    quick_sort_recursive(my_list, pivot+1, hi, sort_crit)
    
    
def merge_sort_linked(my_list, sort_crit):
    """
    Aplica Merge Sort en una lista enlazada siguiendo sort_crit.
    """
    if size(my_list) <= 1:
        return my_list

    left_half, right_half = split_linked_list(my_list)
    
    left_half = merge_sort_linked(left_half, sort_crit)
    right_half = merge_sort_linked(right_half, sort_crit)
    
    return merge_linked(left_half, right_half, sort_crit)

def split_linked_list(my_list):
    """
    Divide la lista en dos mitades y retorna ambas como listas enlazadas.
    """
    if is_empty(my_list) or size(my_list) == 1:
        return my_list, new_list()

    slow = my_list['first']
    fast = my_list['first']
    prev = None

    while fast and fast['next']:
        prev = slow
        slow = slow['next']
        fast = fast['next']['next']

    left_half = my_list
    right_half = new_list()
    right_half['first'] = slow
    right_half['last'] = my_list['last']
    
    if prev:
        prev['next'] = None  # Separar las dos mitades
        left_half['last'] = prev

    left_half['size'] = (size(my_list) + 1) // 2
    right_half['size'] = size(my_list) // 2

    return left_half, right_half

def merge_linked(left_half, right_half, sort_crit):
    """
    Fusiona dos listas enlazadas ordenadas en una sola.
    """
    merged_list = new_list()
    
    left = left_half['first']
    right = right_half['first']

    while left and right:
        if sort_crit(left['info'], right['info']):
            add_last(merged_list, left['info'])
            left = left['next']
        else:
            add_last(merged_list, right['info'])
            right = right['next']

    while left:
        add_last(merged_list, left['info'])
        left = left['next']

    while right:
        add_last(merged_list, right['info'])
        right = right['next']

    return merged_list
