import random

def new_list():
    newlist = {
        'elements': [],
        'size' : 0 
    }
    return newlist

def get_element(my_list, index):
    if 0 <= index < my_list['size']:  
        return my_list['elements'][index]
    else:
        raise IndexError(f"Índice fuera de rango: {index}, tamaño de la lista: {my_list['size']}")

def is_present(my_list, element, cmp_function):
    
    size = my_list['size']
    if size > 0:
        keyexist = False 
        for keypos in range(0, size):
            info = my_list['elements'][keypos]
            if cmp_function(info, element) == 0:
                keyexist = True
                break
        if keyexist:
            return keypos
    return -1


               
def add_first(my_list, element):
    my_list['elements'].insert(0, element)  
    my_list['size'] += 1
    return my_list


def add_last(my_list, element):


    my_list['elements'].append(element)
    my_list['size'] += 1

    return my_list # This function modifies my_list in place and returns it.



def size(my_list):
    return my_list['size']

def first_element (my_list):
    if my_list['size'] > 0:
        return my_list['elements'][0]
    
    
def is_empty(my_list):
    vacia = False
    if my_list['size'] == 0:
        vacia = True
    return vacia

def remove_first(my_list):
    element = my_list['elements'][0]
    my_list['elements'] = my_list['elements'][1:]
    my_list['size'] -= 1
    return element
    
def remove_last(my_list):
    """
    Removes and returns the last element from the list.
    """
    if my_list['size'] == 0: # Check if list is empty
        raise Exception('EmptyStructureError: array_list is empty') # Consistent error for empty list
    
    element = my_list['elements'].pop() # <--- CRITICAL FIX: Use Python's list.pop() to remove and return the last element
    # Python's list.pop() already removes the element from the list.
    
    my_list['size'] -= 1 # Decrement logical size
    
    return element
        
def insert_element(my_list, element, pos):
    size = my_list['size']
    if (pos > size -1) or (pos < 0):
        return my_list
    else:
        my_list['elements'][pos] = element
    my_list['size'] += 1
    return my_list

def delete_element(my_list, pos):
    size = my_list['size']
    if 0 <= pos < size:
        my_list['elements'].pop(pos)  
        my_list['size'] -= 1
    return my_list
    
def change_info(my_list, pos, new_info):
    size = my_list['size']
    if 0 <= pos and pos < size:
        my_list['elements'][pos] = new_info
    return my_list
      
        
def exchange(my_list, pos_1, pos_2):
    size = my_list['size']
    if pos_1 >= 0 and pos_1 < size and pos_2 >= 0 and pos_2 < size:
        my_list['elements'][pos_1], my_list['elements'][pos_2] = my_list['elements'][pos_2],  my_list['elements'][pos_1]
        
    return my_list

def sub_list(my_list, pos_i, num_elements):
    size = my_list['size']
    if 0 <= pos_i < size and 0 < num_elements <= size - pos_i:
        return {
            'elements': my_list['elements'][pos_i:pos_i + num_elements],
            'size': num_elements
        }
    return new_list()

def default_sort_criteria(element_1, element_2):
    is_sorted = False 
    if element_1 < element_2:
        is_sorted = True
    return is_sorted

#ORDENAMIENTOS ITERATIVOS (SELECTION, INSERTION, SHELL) sort()


def selection_sort (my_list, sort_crit):

    n = my_list['size']
    elements = my_list['elements']
    
    for i in range(n - 1):
        min_elem = i
        for j in range(i + 1, n):
            if sort_crit(elements[j], elements[min_elem]):
                min_elem = j
        if min_elem !=i:
            elements[i], elements[min_elem] = elements[min_elem], elements[i]
                
    return elements


def insertion_sort (my_list, sort_crit):
    size = my_list["size"]
    
    for i in range (1,size):
        key = my_list['elements'][i]
        j = i - 1
        while j >= 0 and sort_crit(my_list['elements'][j], key) > 0:
            my_list['elements'][j + 1] = my_list['elements'][j]
            j -= 1
        my_list['elements'][j + 1] = key
    return my_list


def shell_sort(my_list, sort_crit):
    tamanio = size(my_list)
    h = 1
    while (h < tamanio//3): # Calcula el primer valor de h, para hacer los h-sort subarreglos- ish. 
        h = 3*h + 1 #Formula para caluclar el siguiente H, en este caso seria siempre aproximando hacia arriba. 
        
    while h>= 1:
        for i in range(h,tamanio):
            j = i
            while (j >= h) and sort_crit(get_element(my_list,j), get_element(my_list,j-h)):
                exchange(my_list,j,j-h)
                
                j -= h
        h //= 3
    
    return my_list
            
            


#ORDENAMIENTOS RECURSIVOS (MERGE, QUICK) sort().
#Merge sort en array_list() implementación del libro de Sedgewick y Waine (porque no entendi la de la clase) 
def merge_sort(my_list,sort_crit):
    aux_lst = {'elements': my_list['elements'][:], 'size': my_list['size']}  # Crear la lista auxiliar donde se van a ir almacenando lois datos, Este algoritmo no es in-place.
    merge_sort_recursivo(my_list, aux_lst, sort_crit,0,my_list['size'] -1) # Recursividad 
    
    lista_ordenada = new_list()
    for elemento in my_list['elements']:
        add_last(lista_ordenada, elemento)
    
    return lista_ordenada
    

def merge_sort_recursivo(my_list, aux_lst, sort_crit, lo, hi): #Ordena los elementos de la primera y de la segunda mitad tipo [[1,2,3,4], [8,9,10,11,12]]
    if hi <= lo:
        return 
    mid = lo + (hi - lo) // 2 # La particion en las dos mitades / midpoint
    merge_sort_recursivo(my_list, aux_lst, sort_crit, lo, mid) # Ordenamiento de la primera mitad de forma recursiva
    merge_sort_recursivo(my_list, aux_lst, sort_crit, mid +1, hi) # Ordeamiento de la segunda mitad tambien recursivo. 
    merge_sort_mezcla(my_list,aux_lst, sort_crit, lo , mid, hi) #Los que se curzan entre lasl istas 
    
def merge_sort_mezcla(my_list,aux_lst,sort_crit, lo, mid, hi): # Ordena los que estan en una mitad y en otra, orden lineal (JODAAAAA) RE TRYHARD
    aux_lst['elements'][lo:hi + 1] = my_list['elements'][lo:hi + 1] # Creo la lista auxiliar, como una ''copia' pero no directamente porque una sublist me daria un Index error

    i, j = lo, mid + 1 #Apuntadores entre las dos listas, donde empieza a comparar el elemento de una lista con la otra

    for k in range(lo, hi + 1):
        if i > mid:  # Ordena la mitad de la izquierda comparando con la derecha 
            change_info(my_list, k, get_element(aux_lst, j))
            j += 1 # Incrementa por cada valor de la izquierda, todos los de la derecha, compara el primer valor con todos los de la derecha, y despues sube uno en la izq y asi hasta acabr, si hay necesidad hace el swap. 
        elif j > hi:  #Lo mismo pero con la derecha 
            change_info(my_list, k, get_element(aux_lst, i))
            i += 1
        elif sort_crit(get_element(aux_lst, j), get_element(aux_lst, i)): # Revisa si hay uno mayor que otro en los dos lados, y hce el "swap" de la informacion
            change_info(my_list, k, get_element(aux_lst, j))
            j += 1
        else:
            change_info(my_list, k, get_element(aux_lst, i)) # lo mismo pero del otro lado, si no esta ordenado. 
            i += 1

#HISTORICOOOOOO  


# QUICK SORT

def quick_sort(my_list,sort_crit):
    quick_sort_recursivo(my_list,0,my_list['size']-1,sort_crit) 
    return my_list
    
def quick_sort_recursivo(my_list,lo,hi,sort_crit):
    if lo >= hi:
        return 
    
    pivote = partition(my_list,lo,hi,sort_crit) 
    quick_sort_recursivo(my_list,lo,pivote -1 , sort_crit)
    quick_sort_recursivo(my_list,pivote +1, hi, sort_crit)
    
def partition(my_list,lo,hi,sort_crit):
    atras = lo
    adelante = lo
    
    while adelante < hi:
        if sort_crit(get_element(my_list,adelante), get_element(my_list, hi)):
            exchange(my_list,atras,adelante)
            atras += 1
        adelante += 1
    
    exchange(my_list,atras,hi)
    
    return atras 


 

# Binary para una lista ordenada nativa de python
def binary_search(my_list,elem,lo , hi):
    #Caso base
    if lo > hi: 
        return -1 
    mid = (lo + hi) // 2
    if my_list[mid] == elem:
        return mid
    elif my_list[mid] > elem:
        return binary_search(my_list, elem, lo, mid-1)
    else:
        return binary_search(my_list,elem, mid + 1, hi)

#Binary search para implementarlo en el reto. 
def binary_search_reto_2(my_list, target_year):
    # Validar si esta o no esta (sacado de stackoverflow)
    if not my_list or not isinstance(my_list, dict) or 'elements' not in my_list:
        return -1
    #ESTE PEDAZO YA NO FUE SACADO DE STACK OVERFLOW. 
    
    elements = my_list['elements']
    if not elements:
        return -1
    

    low = 0
    high = len(elements) - 1
    
   
    while low <= high:
        mid = (low + high) // 2
        current_year = elements[mid]['year_collection']
        
        if current_year == target_year:
            return mid
        elif current_year < target_year:
            low = mid + 1
        else:
            high = mid - 1
    
    return -1 

#Binary search reqerimiento 6
def binary_search_req_6(my_list, target_year):
    # Validar si esta o no esta (sacado de stackoverflow)
    if not my_list or not isinstance(my_list, dict) or 'elements' not in my_list:
        return -1
    #ESTE PEDAZO YA NO FUE SACADO DE STACK OVERFLOW. 
    
    elements = my_list['elements']
    if not elements:
        return -1
    

    low = 0
    high = len(elements) - 1
    
   
    while low <= high:
        mid = (low + high) // 2
        current_year = elements[mid]['load_time']
        
        if current_year == target_year:
            return mid
        elif current_year < target_year:
            low = mid + 1
        else:
            high = mid - 1
    
    return -1 