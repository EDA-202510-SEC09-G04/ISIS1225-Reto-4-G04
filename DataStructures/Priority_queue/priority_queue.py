# DataStructures/Priority_queue/priority_queue.py (DEFINITIVE FIX)

from DataStructures.List import array_list as lt
from DataStructures.Priority_queue import index_pq_entry as pq 

def new_heap (is_min_pq = True):
    queue = {
        'elements': lt.new_list(), # This creates the actual array_list object
        'size': 0, # This is the heap's conceptual size (number of valid entries, excluding index 0)
        'cmp_function': default_compare_lower_value if is_min_pq else default_compare_higher_value
    }
   
    # The index 0 is left empty in 1-based indexing heaps.
    lt.add_last(queue['elements'], None) # Add a dummy None element at index 0
    # print(f"  PQ_NEW_HEAP_DEBUG: Created new heap. 'elements' array_list ID: {id(queue['elements'])}. Internal array_list size: {lt.size(queue['elements'])}") # DEBUG
    return queue

def default_compare_lower_value (father_node, child_node):
    f = pq.get_key(father_node) 
    c = pq.get_key(child_node)
    return f <= c # True if father is smaller or equal (higher priority for MIN-heap)

def default_compare_higher_value (father_node, child_node):
    f = pq.get_key(father_node)
    c = pq.get_key(child_node)
    return f >= c # True if father is greater or equal (higher priority for MAX-heap)
    
def priority (my_heap, parent_entry, child_entry):
    cmp_function = my_heap['cmp_function']
    return cmp_function(parent_entry, child_entry) # This function correctly defines "parent has higher priority than child"


def put (my_heap, priority_value, item_value):
    # print(f"  PQ_PUT_DEBUG: Attempting to put ({priority_value}, '{item_value}'). Current heap conceptual size: {my_heap['size']}") # DEBUG
    # print(f"  PQ_PUT_DEBUG: 'elements' array_list ID BEFORE ADD_LAST: {id(my_heap['elements'])}. Internal array_list size: {lt.size(my_heap['elements'])}") # DEBUG

    new_entry = pq.new_pq_entry(priority_value, item_value)
    
    # Add to the end of the array_list. lt.add_last modifies my_heap['elements'] in place.
    lt.add_last(my_heap['elements'], new_entry) 
    
    # After adding an element to the underlying array_list, the heap's conceptual size increases.
    # The new element is at the very end, at index lt.size(my_heap['elements']) - 1.
    my_heap['size'] = lt.size(my_heap['elements']) - 1 # <--- FIX: my_heap['size'] is now (array_list_size - 1 for dummy)
    
    # print(f"  PQ_PUT_DEBUG: 'elements' array_list ID AFTER ADD_LAST: {id(my_heap['elements'])}. Internal array_list size: {lt.size(my_heap['elements'])}") # DEBUG
    # print(f"  PQ_PUT_DEBUG: New heap conceptual size (after put): {my_heap['size']}") # DEBUG

    # Swim the newly added element up from its position (which is at the end of the current actual elements)
    # The position to swim from is the last valid element's index, which is my_heap['size'].
    # print(f"  PQ_PUT_DEBUG: Heap before swim (conceptual size {my_heap['size']}, array_list size {lt.size(my_heap['elements'])}): {[pq.get_key(lt.get_element(my_heap['elements'], i)) for i in range(1, lt.size(my_heap['elements']))]}") # DEBUG
    swim(my_heap, my_heap['size']) # <--- Pass correct position for swim (last element's index)
    # print(f"  PQ_PUT_DEBUG: Heap after swim (conceptual size {my_heap['size']}, array_list size {lt.size(my_heap['elements'])}): {[pq.get_key(lt.get_element(my_heap['elements'], i)) for i in range(1, lt.size(my_heap['elements']))]}") # DEBUG
    
    return my_heap


def swim(my_heap: dict, pos: int):
    """
    Sube el elemento en 'pos' hasta restaurar la propiedad del heap.
    """
    elems = my_heap['elements'] # This is the array_list object
    # print(f"    PQ_SWIM_DEBUG: Starting swim for pos {pos}. 'elements' array_list ID: {id(elems)}. Heap before any swap (array_list content): {[pq.get_key(lt.get_element(elems, i)) for i in range(1, lt.size(elems))]}") # DEBUG

    # While not at the root (pos > 1) AND the parent does NOT satisfy the priority property over the child:
    # (i.e., for min-heap, if parent.key > child.key, then priority() returns False)
    while pos > 1 and not priority(
        my_heap,
        lt.get_element(elems, pos // 2),  # parent entry
        lt.get_element(elems, pos)         # child entry
    ):
        # print(f"      PQ_SWIM_DEBUG: Swapping {pq.get_key(lt.get_element(elems, pos // 2))} (pos {pos // 2}) with {pq.get_key(lt.get_element(elems, pos))} (pos {pos})") # DEBUG
        lt.exchange(elems, pos // 2, pos) # lt.exchange operates on the array_list
        pos //= 2 # Move up one level
    # print(f"    PQ_SWIM_DEBUG: Swim finished. Heap after swim (array_list content): {[pq.get_key(lt.get_element(elems, i)) for i in range(1, lt.size(elems))]}") # DEBUG


def size (my_heap):
    return my_heap['size']

def is_empty (my_heap):
    return my_heap['size'] == 0
    
def get_first_priority (my_heap):
    if my_heap['size'] > 0:
        return pq.get_key(lt.get_element(my_heap['elements'], 1))
    return None # Return None if heap is empty
        

def del_min (my_heap):
    """
    Elimina y retorna el elemento de mayor prioridad (raíz) del heap.
    Para un min-heap, este es el elemento con la prioridad más baja.
    """
    if my_heap['size'] == 0:
        # print(f"  PQ_DEL_MIN_DEBUG: Heap is empty. Returning None, None.") # DEBUG
        return None, None 
    
    # print(f"  PQ_DEL_MIN_DEBUG: 'elements' array_list ID BEFORE DEL_MIN: {id(my_heap['elements'])}") # DEBUG

    first_entry = lt.get_element(my_heap['elements'], 1) # Root element to extract
    priority_value = pq.get_key(first_entry)
    item_value = pq.get_index(first_entry)

    # Use lt.size(my_heap['elements']) for print range
    # print(f"  PQ_DEL_MIN_DEBUG: Extracting ({priority_value}, '{item_value}'). Heap before ops (conceptual size {my_heap['size']}, array_list size {lt.size(my_heap['elements'])}): {[pq.get_key(lt.get_element(my_heap['elements'], i)) for i in range(1, lt.size(my_heap['elements']))]}") # DEBUG

    # Swap the root element (index 1) with the last valid element (index my_heap['size'])
    lt.exchange(my_heap['elements'], 1, my_heap['size']) 
    
    # print(f"  PQ_DEL_MIN_DEBUG: After exchange: elements array_list ID: {id(my_heap['elements'])}. elements={my_heap['elements']['elements']} size={my_heap['elements']['size']}") # DEBUG

    # Physically remove the last element from the array_list
    # (which is now the original root, after the swap)
    lt.remove_last(my_heap['elements']) 
    
    # print(f"  PQ_DEL_MIN_DEBUG: After remove_last: elements array_list ID: {id(my_heap['elements'])}. elements={my_heap['elements']['elements']} size={my_heap['elements']['size']}") # DEBUG

    my_heap['size'] -= 1 # Decrement heap's conceptual size
    
    # Restore heap property by sinking the new root (if elements remain)
    if my_heap['size'] > 0: 
        sink(my_heap, 1) # Sink from the root (pos 1)
    
    # Use lt.size(my_heap['elements']) for print range
    # print(f"  PQ_DEL_MIN_DEBUG: Heap after ops (conceptual size {my_heap['size']}, array_list size {lt.size(my_heap['elements'])}): {[pq.get_key(lt.get_element(my_heap['elements'], i)) for i in range(1, lt.size(my_heap['elements']))]}") # DEBUG
        
    return (priority_value, item_value) 


def sink(my_heap: dict, pos: int):
    elems = my_heap['elements'] # This is the array_list object
    size  = my_heap['size'] # This is the conceptual heap size (number of valid elements)

    # print(f"    PQ_SINK_DEBUG: Starting sink for pos {pos}. 'elements' array_list ID: {id(elems)}. Heap before any swap (array_list content): {[pq.get_key(lt.get_element(elems, i)) for i in range(1, lt.size(elems))]}") # DEBUG

    left_child_pos = 2 * pos # Index of left child

    # Continue while the current node has at least a left child within the conceptual heap bounds
    while left_child_pos <= size: 
        right_child_pos = left_child_pos + 1 # Index of right child

        fav_child_pos = left_child_pos # Assume left child is favorite initially
        
        # If right child exists within bounds AND left child does NOT have priority over right:
        # (i.e., right child has HIGHER priority than left child)
        if right_child_pos <= size and not priority(
            my_heap,
            lt.get_element(elems, left_child_pos),   # Treat left child as "parent" for comparison
            lt.get_element(elems, right_child_pos)   # Treat right child as "child" for comparison
        ):
            fav_child_pos = right_child_pos # Then right child is the favorite (has higher priority)

        # If the node at 'pos' already satisfies the priority property relative to its favorite child,
        # the heap property is met, so we break the loop.
        # 'priority' returns TRUE if parent is 'better' than child.
        if priority(
            my_heap,
            lt.get_element(elems, pos),     # parent entry (element at current position)
            lt.get_element(elems, fav_child_pos)      # favorite child entry
        ):
            break # Heap property holds, no more sinking needed
        else:
            # If not (the favorite child has higher priority),
            # swap current node with its favorite child and continue sinking
            # print(f"      PQ_SINK_DEBUG: Swapping {pq.get_key(lt.get_element(elems, pos))} (pos {pos}) with {pq.get_key(lt.get_element(elems, fav_child_pos))} (fav child pos {fav_child_pos})") # DEBUG
            lt.exchange(elems, pos, fav_child_pos)
            pos  = fav_child_pos # Move down to the favorite child's position
            left_child_pos = 2 * pos # Update left child index for next iteration
    # print(f"    PQ_SINK_DEBUG: Sink finished. Heap after sink (array_list content): {[pq.get_key(lt.get_element(elems, i)) for i in range(1, lt.size(elems))]}") # DEBUG