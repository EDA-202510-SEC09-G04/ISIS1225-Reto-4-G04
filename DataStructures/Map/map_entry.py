# DataStructures/Map/map_entry.py

def new_map_entry(key, value, state='occupied'):
    entry = {'key': key, 'value': value, 'state': state}
    return entry

def set_key(my_entry, key):
    my_entry['key'] = key
    return my_entry

def set_value(my_entry, value):
    my_entry['value'] = value
    return my_entry

def get_key(my_entry):
    return my_entry['key']

def get_value(my_entry):
    return my_entry['value']