# DataStructures/Map/map_linear_probing.py

from DataStructures.Map import map_functions as mp
import random as rd
from DataStructures.List import array_list as lt
from DataStructures.Map import map_entry as me

def _put_internal_logic(my_map, key, value):
    initial_hash = (my_map['scale'] * hash(key) + my_map['shift']) % my_map['prime']
    index = initial_hash % my_map['capacity']

    found_deleted_slot = -1
    
    probes = 0
    while probes < my_map['capacity']: 
        entry = my_map['table']['elements'][index]

        if entry is None:
            if found_deleted_slot != -1:
                index = found_deleted_slot
            
            my_map['table']['elements'][index] = me.new_map_entry(key, value, 'occupied')
            my_map['size'] += 1
            return

        elif entry['state'] == 'occupied':
            if entry['key'] == key:
                my_map['table']['elements'][index]['value'] = value
                return

        elif entry['state'] == 'deleted':
            if found_deleted_slot == -1:
                found_deleted_slot = index
            # Continue probing, the key might be further down
        
        index = (index + 1) % my_map['capacity']
        probes += 1
    
    if found_deleted_slot != -1:
        my_map['table']['elements'][found_deleted_slot] = me.new_map_entry(key, value, 'occupied')
        my_map['size'] += 1
        return

    raise Exception("Map is full or probing failed to find a slot!")


def new_map(num_elements, load_factor, prime=109345121):
    capacity = mp.next_prime(int(num_elements / load_factor))
    scale = rd.randint(1, prime - 1)
    shift = rd.randint(0, prime - 1)
    
    hash_table = {
        'prime': prime,
        "capacity": capacity,
        "scale": scale,
        "shift": shift,
        "table": lt.new_list(),
        "current_factor": 0,
        "limit_factor": load_factor,
        'size': 0,
        'type': 'PROBE_HASH_MAP'
    }
    
    hash_table['table']['elements'] = [None] * capacity
    hash_table['table']['size'] = capacity

    return hash_table

def put(my_map, key, value):
    if my_map['size'] / my_map['capacity'] >= my_map['limit_factor']:
        my_map = rehash(my_map)

    _put_internal_logic(my_map, key, value)

    my_map['current_factor'] = my_map['size'] / my_map['capacity']
    
    return my_map

def find_slot(my_map, key, hash_value):
   first_avail = None
   current_pos = hash_value
   probes = 0
   while probes < my_map["capacity"]:
      entry = lt.get_element(my_map["table"], current_pos)
      
      if entry is None:
            if first_avail is None:
               first_avail = current_pos
            return False, first_avail 
      
      if entry['state'] == 'occupied':
            if entry['key'] == key:
                return True, current_pos
      elif entry['state'] == 'deleted':
            if first_avail is None:
               first_avail = current_pos
      
      current_pos = (current_pos + 1) % my_map["capacity"]
      probes += 1
      
   return False, first_avail if first_avail is not None else -1

def get(my_map, key):
    hash_value = (my_map['scale'] * hash(key) + my_map['shift']) % my_map['prime']
    index = hash_value % my_map['capacity']
    probes = 0
    
    while probes < my_map['capacity']:
        entry = my_map['table']['elements'][index]
        
        if entry is None:
            return None
        
        if entry['state'] == 'occupied' and entry['key'] == key:
            return entry['value']
        
        index = (index + 1) % my_map['capacity']
        probes += 1
        
    return None

def remove(my_map, key):
    hash_value = (my_map['scale'] * hash(key) + my_map['shift']) % my_map['prime']
    index = hash_value % my_map['capacity']
    probes = 0
    
    while probes < my_map['capacity']:
        entry = my_map['table']['elements'][index]
        
        if entry is None:
            return my_map
        
        if entry['state'] == 'occupied' and entry['key'] == key:
            my_map['table']['elements'][index]['state'] = 'deleted'
            my_map['size'] -= 1
            my_map['current_factor'] = my_map['size'] / my_map['capacity']
            return my_map
            
        index = (index + 1) % my_map['capacity']
        probes += 1
        
    return my_map

def size(my_map):
    return my_map['size']

def is_empty(my_map):
    return my_map['size'] == 0

def contains(my_map, key):
    return get(my_map, key) is not None

def key_set(my_map):
    keys_list = lt.new_list()
    for i in range(my_map['capacity']):
        entry = my_map['table']['elements'][i]
        if entry is not None and entry['state'] == 'occupied':
            lt.add_last(keys_list, entry['key'])
    return keys_list

def value_set(my_map):
    values_list = lt.new_list()
    for i in range(my_map['capacity']):
        entry = my_map['table']['elements'][i]
        if entry is not None and entry['state'] == 'occupied':
            lt.add_last(values_list, entry['value'])
    return values_list

def rehash(my_map):
    old_capacity = my_map['capacity']
    old_table_elements = my_map['table']['elements']

    new_capacity_val = mp.next_prime(2 * old_capacity)
    
    new_map_obj = new_map(new_capacity_val, my_map['limit_factor'], my_map['prime'])
    new_map_obj['scale'] = my_map['scale']
    new_map_obj['shift'] = my_map['shift']

    for entry in old_table_elements:
        if entry is not None and entry['state'] == 'occupied':
            _put_internal_logic(new_map_obj, entry['key'], entry['value'])

    new_map_obj['current_factor'] = new_map_obj['size'] / new_map_obj['capacity']

    return new_map_obj

def default_compare(key, entry):
    entry_key = entry['key']
    if key == entry_key:
      return 0
    elif key > entry_key:
      return 1
    return -1