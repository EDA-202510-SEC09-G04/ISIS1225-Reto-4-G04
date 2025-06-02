# DataStructures/Stack/stack.py

from DataStructures.List import single_linked_list as lt

# ... (other imports) ...

def new_stack():
    return lt.new_list()

def push(my_stack, element):
    # For O(1) push in a LIFO stack using a single linked list,
    # you typically add to the END of the list (which is where your 'last' pointer is efficient).
    # Or, if you want push/pop from the beginning (which is usually where SLLs are efficient for LIFO)
    # the push should set the 'first' node to the new element and its next to the old first.
    # Let's use the 'add_last' and 'remove_last' approach for clarity with your current methods,
    # though technically add_last is O(N) in your SLL without a 'last' pointer,
    # but your SLL does have 'last' so it's O(1) in your SLL.
    
    lt.add_last(my_stack, element) # <--- CHANGE TO ADD_LAST for LIFO with pop from last
    return my_stack

def pop(my_stack):
    # For O(1) pop in a LIFO stack using a single linked list,
    # you should remove from the END of the list (if pushed to end).
    if lt.is_empty(my_stack):
        raise Exception('EmptyStructureError: stack is empty')
    return lt.remove_last(my_stack) # <--- CHANGE TO REMOVE_LAST for LIFO

def is_empty(my_stack):
    return lt.is_empty(my_stack)

def top(my_stack):
    # The "top" of the stack is now the LAST element in the linked list
    if lt.is_empty(my_stack):
        raise Exception('EmptyStructureError: stack is empty')
    # Access the 'info' from the last node
    return my_stack['last']['info'] # <--- DIRECTLY ACCESS THE LAST NODE'S INFO

def size(my_stack):
    return lt.size(my_stack)    