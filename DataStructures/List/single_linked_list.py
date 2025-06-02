def new_list():
    newlist = {
        'first': None,
        'last': None,
        'size': 0,
        
    }
    return newlist

def get_element(my_list, pos):
    if pos < 0 or pos >= my_list['size']:
        raise Exception('IndexError: list index out of range')
    searchpos = 0
    node = my_list['first']
    while searchpos < pos and node is not None:
        node = node['next']
        searchpos += 1
    if node is None:
        raise Exception('IndexError: list index out of range')  # Evita retornar None

    return node['info']

def is_present (my_list, element, cmp_function):
    is_in_array = False # Este es el centinela (Flag)
    temp = my_list['first']
    count = 0
    while not is_in_array and temp is not None:
        if (cmp_function(element, temp['info']) == 0):
            is_in_array = True
        else:
            temp = temp['next']
            count += 1
    
    if not is_in_array:
        count = -1
    return count
 
def add_first(my_list, element):
    #Paso 1: Revisar si la lista esta vacia (en este caso el primer y el ultimo nodo son el mismo nuevo nodo)
    if my_list['size'] == 0:
        #Paso 1.1: Crear el nuevo nodo
        new_node = {'info': element, 'next': None}
        #Paso 1.2: Hacer que el primer y el ultimo nodo sean el nuevo nodo, como no hay mas nodos, el siguiente nodo es None y se llego al final de la lista.
        my_list['first'] = new_node
        my_list['last'] = new_node
        #Paso 1.3: Incrementar el tamaño de la lista
        my_list['size'] += 1
    #Paso 2: Si la lista no esta vacia
    else:
        #Paso 2.1: Crear el nuevo nodo
        new_node = {'info': element, 'next': None}
        #Paso 2.2: Hacer que el nuevo nodo apunte al anterior primer nodo.
        new_node['next'] = my_list['first']
        #Paso 2.3 Hacer que el primer nodo sea el nuevo nodo
        my_list['first'] = new_node
        #Paso 2.4 Incrementar el tamaño de la lista
        my_list['size'] += 1
    return my_list

def add_last(my_list, element):
    #Paso 1: Crear el nodo
    new_node = {"info": element,
                "next": None }
    #Paso 2: Si la lista esta vacia
    if my_list['size'] == 0:
        my_list['first'] = new_node
        my_list['last'] = new_node
        # Paso 3. Incrementar el tamaño de la lista
        my_list['size'] +=1
    # Paso 4: Si la lista no esta vacia
    else: 
        # Necesitamos movernos a traves de la lista para llegar al final, entonces:
        size = my_list['size']
        index = my_list['first']
        # Paso 5: Moverse a traves de la lista
        for i in range(size -1): #Se pone size -1 porque el indice empieza en 0, pero se podria hacer mas facil, reordenando la lista y dandole add_first().
            index = index['next'] # Este es el avance que siempre va a ser el siguiente nodo. (Estamos referenciando el apuntador)
        #Paso 6: Cambiar el apuntador a nuestro nuevo nodo.
        index['next'] = new_node
        #Paso 7: Hacer que el nuevo nodo sea el ultimo nodo
        my_list['last'] = new_node
        #Paso 8: Incrementar el tamaño de la lista
        my_list['size'] += 1
    return my_list
        
def size(my_list):
    return my_list['size'] # Historico 

def first_element(my_list):
    if my_list['size'] > 0:
        return my_list['first']
   
   
   
   
   
def compare_function(elemento_1, elemento_2):
    if elemento_1['info'] == elemento_2['info']:
        return 0 
    if elemento_1['info'] < elemento_2['info']:
        return -1
    else:
        return 1

def insert_element_sorted_list(lst, element, comp_function): 
    new_node = {"info": element,
                'next': None}
    
    if lst['size'] == 0:
        lst['first'] = new_node
        lst['last'] = new_node 
        lst['size'] += 1
    else:
        if comp_function(element, lst['first']) == -1:
            new_node['next'] = lst['first']
            lst['first'] = new_node
            
        else:
            prev = lst['first']
            temp = lst['first']['next']
            while temp != None and compare_function(new_node, temp) == 1:
             prev = temp
             temp = temp['next']
            prev['next'] = new_node
            new_node['next'] = temp
        
        if temp == None:
            lst['last'] = new_node
    lst['size'] += 1
    
    return lst
            
def remove_first(my_list):
    node = my_list['first']
    if my_list['size'] == 0:
         raise Exception('EmptyStructureError: stack is empty')
    else:
        my_list['first'] = node['next']
        my_list['size'] -= 1
        return node['info']
        
def remove_last(my_list):
    if my_list['size'] == 0:
        raise Exception('EmptyStructureError: stack is empty')
    else: 
        temp = my_list['first']
        if temp['next'] is None:
            return remove_first(my_list)
        else:
            while temp['next']['next'] is not None:
                temp = temp['next']
            node = temp['next']
            temp['next'] = None
            my_list['size'] -= 1
            return node['info']

def exchange(my_list,pos_1,pos_2):
    if pos_1 < 0 or pos_1 >= my_list['size'] or pos_2 < 0 or pos_2 >= my_list['size']:
       raise Exception('IndexError: list index out of range')
   
    if pos_1 == pos_2:
        return my_list
    
    ahorita = my_list['first']
    nodo_1 = None
    nodo_2 = None
    count = 0
    
    while ahorita is not None:
        if count == pos_1:
            nodo_1 = ahorita
        if count == pos_2:
            nodo_2 = ahorita
        
        ahorita = ahorita["next"]
        count += 1
    
    if nodo_1 is not None and nodo_2 is not None:
        nodo_1['info'], nodo_2['info'] = nodo_2['info'], nodo_1['info']
        
    return my_list


def change_info(my_list,pos,new_info):
    if pos <0 or pos >= my_list['size']:
        raise Exception("IndexError: List Index out of Range.")
    
    ahorita = my_list['first']
    indice = 0
    while indice < pos:
        ahorita = ahorita['next']
        index += 1
        
    ahorita['info'] = new_info
    
    return my_list
        
        
                      
def default_sort_criteria(element_1, element_2):
    is_sorted = False 
    if element_1 < element_2:
        is_sorted = True
    return is_sorted  

#Algoritmos de ordenamiento para SLL 
#

#Algoritmos iterativos - {Selection, Insertion, Shell} Sort()

def selection_sort (my_list, sort_crit):
    
    if my_list ["size"] < 2:
        return my_list
        
    x = my_list["first"]
    while x:
        min_elem = x
        next_elem = x["next"]
        
        while next_elem:
            if sort_crit (next_elem["info"], min_elem["info"]):
                min_elem = next_elem
            next_elem = next_elem["next"]
                
        if min_elem !=x:
            x["info"], min_elem["info"] = min_elem["info"], x["info"]
        x = x["next"] 
                        
    return my_list    
            

def insertion_sort(my_list,sort_crit):
    tamanio = my_list['size']
    
    for i in range(1,tamanio):
        j = i
        while j > 0 and sort_crit(get_element(my_list,j), get_element(my_list, j -1)):
            exchange(my_list, j, j-1)
            j -= 1
    
    return my_list


def shell_sort(my_list, sort_crit):
    tamanio = my_list['size']
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

#Algoritmos de ordenamiento Recursivos {Merge, quick} sort()
#Primero MERGE SOOORTTT 
def merge_sort(my_list, sort_crit):
    if my_list['size'] < 2: #Un elemento ya esta ordenada esa monda.
        return my_list
    #Dividir la lista en las dos mitadoes con la funcion auxiliar 
    mitad_izq, mitad_der = dividir_lista(my_list)
    
    #Ordenar las dos mitades con recursiooooonnn
    ordenar_izq = merge_sort(mitad_izq,sort_crit)
    ordenar_der = merge_sort(mitad_der,sort_crit)
    
    return merge_sort_combinado(ordenar_izq,ordenar_der, sort_crit)

def dividir_lista(my_list):
    mid = my_list['size'] // 2
    lista_izq = new_list()
    lista_der = new_list()
    
    ahorita = my_list['first']
    count = 0
    
    while ahorita != None:
        if count < mid:
            add_last(lista_izq, ahorita['info'])
        else:
            add_last(lista_der, ahorita["info"])
        
        ahorita = ahorita['next']
        count += 1
        
    return lista_izq, lista_der

def merge_sort_combinado(izq,der,sort_crit):
    lista_ordenada = new_list()
    nodo_izq = izq['first']
    nodo_der = der['first']
    
    while nodo_izq != None and nodo_der != None:
        if sort_crit(nodo_izq['info'], nodo_der['info']):
            add_last(lista_ordenada,nodo_izq['info'])
            nodo_izq = nodo_izq['next']
        else:
            add_last(lista_ordenada, nodo_der['info'])
            nodo_der = nodo_der['next']
    
    while nodo_izq != None:
        add_last(lista_ordenada,nodo_izq["info"])
        nodo_izq = nodo_izq['next']
    
    while nodo_der != None:
        add_last(lista_ordenada,nodo_der['info'])
        nodo_der= nodo_der["next"]
        
    return lista_ordenada

# QUICK SOOOORTTT

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
        
        
def is_empty(my_list):
    """
    Checks if the single linked list is empty.
    Returns True if the list is empty, False otherwise.
    """
    return my_list['size'] == 0


def reverse(my_list):

    reversed_list = new_list() 
    current_node = my_list['first']
    while current_node is not None:
        add_first(reversed_list, current_node['info']) 
        current_node = current_node['next']
        
    return reversed_list