from asyncio import current_task
import math
import random
from DataStructures.List import array_list as al
from DataStructures.Map.map_functions import hash_value, next_prime
from DataStructures.Map import map_entry as me



def find_slot(my_map, key, hash_value):
   first_avail = None
   found = False
   ocupied = False
   while not found:
      if is_available(my_map["table"], hash_value):
            if first_avail is None:
               first_avail = hash_value
            entry = al.get_element(my_map["table"], hash_value)
            if me.get_key(entry) is None:
               found = True
      elif default_compare(key, al.get_element(my_map["table"], hash_value)) == 0:
            first_avail = hash_value
            found = True
            ocupied = True
      hash_value = (hash_value + 1) % my_map["capacity"]
   return ocupied, first_avail

def is_available(table, pos):
   entry = al.get_element(table, pos)
   if me.get_key(entry) is None or me.get_key(entry) == "__EMPTY__":
      return True
   return False

def default_compare(key, entry):

   if key == me.get_key(entry):
      return 0
   elif key > me.get_key(entry):
      return 1
   return -1

def new_map(num_elements, load_factor, prime=109345121):
    if load_factor <= 0:
        raise ValueError("El load_factor debe ser mayor que 0")
    
    raw_capacity = int(num_elements / load_factor)
    if raw_capacity < 1:
        raw_capacity = 3  # capacidad mínima segura
    
    capacity = next_prime(raw_capacity)
    if capacity < 1:
        capacity = 3  # fallback de seguridad

    # Valores fijos para pruebas
    scale = 1
    shift = 0
    table = al.new_list()

    for _ in range(capacity):
        al.add_last(table, {'key': None, 'value': None})

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



def put(my_map, key, value):
    hash_index = hash_value(my_map, key)
    ocupied, slot_index = find_slot(my_map, key, hash_index)
    
    elements = my_map['table']['elements']
    
    if elements[slot_index]['key'] is not None:
        elements[slot_index]['value'] = value
    else:
        elements[slot_index] = {'key': key, 'value': value}
        my_map['size'] += 1
        
        my_map['current_factor'] = my_map['size'] / my_map['table']['size']
        
        if my_map['current_factor'] > my_map['limit_factor']:
            my_map = rehash(my_map)
    
    return my_map



def contains(my_map, key):
    hash_index = hash_value(my_map, key)
    ocupied, slot_index = find_slot(my_map, key, hash_index)

    elements = my_map['table']
    entry = al.get_element(elements, slot_index)

    return me.get_key(entry) is not None

def get(my_map, key):
    hash_index = hash_value(my_map, key)
    ocupied, slot_index = find_slot(my_map, key, hash_index)

    elements = my_map["table"]
    entry = al.get_element(elements, slot_index)

    if me.get_key(entry) is not None:
        return me.get_value(entry)
    
    return None

def remove(my_map, key):
    hash_index = hash_value(my_map, key)
    ocupied, slot_index = find_slot(my_map, key, hash_index)

    elements = my_map["table"]
    entry = al.get_element(elements, slot_index)

    if me.get_key(entry) is not None:
        al.change_info(elements, slot_index, {"key": "__EMPTY__", "value": None})
        my_map["size"] -= 1

    return my_map

def size(my_map):
    return my_map["size"]

def is_empty(my_map):
    return my_map["size"] == 0

def key_set(my_map):
    keys = al.new_list()
    for entry in my_map["table"]["elements"]:
        if entry["key"] is not None and entry["key"] != "__EMPTY__":
            al.add_last(keys, entry["key"])
    return keys

def value_set(my_map):
    values = al.new_list()
    for entry in my_map["table"]["elements"]:
        if entry["key"] is not None and entry["key"] != "__EMPTY__":
            al.add_last(values, entry["value"])
    return values
    
def rehash(my_map):
    new_table = new_map(my_map['capacity'], my_map["limit_factor"])
    
    for entry in my_map["table"]["elements"]:
        if entry["key"] is not None and entry["key"] != "__EMPTY__":
            put(new_table, entry["key"], entry["value"])
    
    return new_table
