import random
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as slist
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
from DataStructures.Utils import error as error

def new_map(num_elements, load_factor, prime=109345121):
    capacity = mf.next_prime(int(num_elements / load_factor))
    
    # Valores fijos para pruebas, de lo contrario, usa valores aleatorios
    scale = random.randint(1, prime - 1)
    shift = random.randint(0, prime - 1)
    table = al.new_list()

    for _ in range(capacity):
        al.add_last(table, slist.new_list())
    
    new_table = {
        'prime': prime,
        'capacity': capacity,
        'scale': scale,
        'shift': shift,
        'table': table,
        'current_factor': 0,
        'limit_factor': load_factor,
        'size': 0
    }
    
    return new_table



def put(map_struct, key, value):
    try:
        pos = mf.hash_value(map_struct, key)

        bucket = al.get_element(map_struct['table'], pos)

        for i in range(slist.size(bucket)):
            entry = slist.get_element(bucket, i)
            if entry['key'] == key:
                entry['value'] = value
                return map_struct 

        new_entry = me.new_map_entry(key, value)
        slist.add_last(bucket, new_entry)

        map_struct['size'] += 1
        map_struct['current_factor'] = float(map_struct['size']) / map_struct['capacity']

        if map_struct['current_factor'] >= map_struct['limit_factor']:
            rehash(map_struct)
            
        return map_struct

    except Exception as e:
        error.reraise(e, 'put')

def default_compare(key, element):
    if (key == me.get_key(element)):
      return 0
    elif (key > me.get_key(element)):
      return 1
    return -1

def contains(map_struct, key):
    try:
        pos = mf.hash_value(map_struct,key)

        bucket = al.get_element(map_struct['table'], pos)

        for i in range(slist.size(bucket)):
            entry = slist.get_element(bucket, i)
            if entry['key'] == key:
                return True

        return False

    except Exception as e:
        error.reraise(e, 'contains')

def remove(map_struct, key):
    try:
        pos = mf.hash_value(map_struct, key)

        bucket = al.get_element(map_struct['table'], pos)
        
        if bucket is None: 
            return map_struct 

        for i in range(slist.size(bucket)):
            entry = slist.get_element(bucket, i)
            if entry['key'] == key:
                slist.delete_element(bucket, i)
                map_struct['size'] -= 1
                return map_struct
        return map_struct

    except Exception as e:
        error.reraise(e, 'remove')

def get(map_struct, key):
    try:
        pos = mf.hash_value(map_struct, key)

        bucket = al.get_element(map_struct['table'], pos)

        for i in range(slist.size(bucket)):
            entry = slist.get_element(bucket, i)
            if entry['key'] == key:
                return entry['value']

        return None

    except Exception as e:
        error.reraise(e, 'get')

def size(map_struct):
    return map_struct['size']

def is_empty(map_struct):
    return map_struct['size'] == 0

def key_set(map_struct):
    try:
        keys = al.new_list()

        for i in range(map_struct['capacity']):
            bucket = al.get_element(map_struct['table'], i)
            for j in range(slist.size(bucket)):
                entry = slist.get_element(bucket, j)
                al.add_last(keys, entry['key'])

        return keys

    except Exception as e:
        error.reraise(e, 'key_set')
        
def value_set(map_struct):
    try:
        values = al.new_list()

        for i in range(map_struct['capacity']):
            bucket = al.get_element(map_struct['table'], i)
            for j in range(slist.size(bucket)):
                entry = slist.get_element(bucket, j)
                al.add_last(values, entry['value'])

        return values

    except Exception as e:
        error.reraise(e, 'value_set')

def rehash(map_struct):
    #la capacidad fue ajustada a 4 veces ya que disminuye las veces que se debe hacer rehash para la cantidad de datos 500,000 que manejamos en este caso xdxdxd
    try:
        new_capacity = mf.next_prime(map_struct['capacity'] * 4)
        new_table = al.new_list()

        for _ in range(new_capacity):
            al.add_last(new_table, slist.new_list())

        old_table = map_struct['table']
        old_capacity = map_struct['capacity']

        map_struct['capacity'] = new_capacity
        map_struct['table'] = new_table
        map_struct['size'] = 0

        for i in range(old_capacity):
            bucket = al.get_element(old_table, i)
            for j in range(slist.size(bucket)):
                entry = slist.get_element(bucket, j)
                put(map_struct, entry['key'], entry['value'])

        map_struct['current_factor'] = map_struct['size'] / map_struct['capacity']

    except Exception as e:
        error.reraise(e, 'rehash')

def map_items(map_struct):
    items = []
    for i in range(map_struct['capacity']):
        bucket = al.get_element(map_struct['table'], i)
        for j in range(slist.size(bucket)):
            entry = slist.get_element(bucket, j)
            items.append((entry['key'], entry['value']))
    return items

