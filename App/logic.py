import time
import os
import csv
import sys
import pprint as pprint
from DataStructures.Map import map_separate_chaining as msc
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as slist
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
from DataStructures.Utils import error as error
from DataStructures.Graph import digraph as gr
from DataStructures.Map import map_linear_probing as mp
from App import utils as ut

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'

defualt_limit = 1000
sys.setrecursionlimit(defualt_limit*10)
csv.field_size_limit(2147483647)


def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    catalog = {
        'domicilios': gr.new_graph(5053)
    } 
    return catalog

# Funciones para la carga de datos

def load_data(catalog):
    """
    Carga los datos del reto
    """
    tiempo_inicial = get_time()
    files = data_dir + 'deliverytime_20.csv'
    input_file = csv.DictReader(open(files, encoding='utf-8'))
    
    my_graph = catalog['domicilios']
    
    total_domicilios = 0
    total_tiempo = []
    
    #diccionario de historial de domiciliarios para los arcos adicionales
    
    historial = {}
    
    print("Creando grafo...")
    for row in input_file:
        total_domicilios += 1
        
        rest_lat = str(row['Restaurant_latitude'])
        rest_lon = str(row['Restaurant_longitude'])
        des_lat = str(row['Delivery_location_latitude'])
        des_lon = str(row['Delivery_location_longitude'])

        #formateo de los ids
        id_rest = ut.format_location(rest_lat, rest_lon) 
        id_des = ut.format_location(des_lat, des_lon) 
        
        #obtener id del domiciliario
        id_domiciliario = row['Delivery_person_ID']
        
        
        #obtener tiempo tomado del domicilio
        time = row['Time_taken(min)']
        total_tiempo.append(int(time))
    

        #creacion nodo del origen con lista de domiciliarios
        ut.crear_nodo(my_graph, id_rest, id_des, id_domiciliario, time, 'restaurante')
        #creacion nodo del destino con  lista de domiciliarios
        ut.crear_nodo(my_graph, id_des, id_rest, id_domiciliario, time, 'destino')
        
        
        
        
        
        #LLMAR A FUNCION DE CREACION DE ARCOS
        my_graph = ut.actualizar_arista(my_graph, id_rest, id_des)
        
        
        
        #CREACION DE ARCOS ADICIONALES ENTRE DESTINOS DE DOMICILIARIOS
        my_graph = ut.procesar_historial(my_graph, historial, id_domiciliario, (id_rest, id_des))
        
        #DESCOMENTAR PARA DEBUG
        """ print(gr.get_vertex_information(my_graph, id_rest))

        
        print('NODO ORIGEN RESTAURANTE')
        ut.print_node_info(my_graph, id_rest)
        print('')
        print('')
        print('')
        print('NODO DESTINO ')
        ut.print_node_info(my_graph, id_des)
        
        ut.debug_arista(my_graph, id_rest, id_des)
        
        print('')
        print('')
        print('DEBUG HISTORIAL RAPPI ')
        debug_historial(historial, id_domiciliario)
        
        # Verificar aristas creadas
        if len(historial.get(id_domiciliario, [])) >= 2:
            last_two = historial[id_domiciliario][-2:]
            dest_anterior = last_two[0][1]
            dest_actual = last_two[1][1]
            ut.debug_arista(my_graph, dest_anterior, dest_actual)
        print('')
        print('')
         """
       
       
    print("Grafo creado.")
    
    #RETORNOS AL FINAL
    
    #domicilios procesados
    #domiciliarios identificados
    total_domiciliarios = len(historial)
    #total nodos
    total_nodos = gr.order(my_graph)
    #total arcos
    total_arcos = (gr.size(my_graph))//2
    #total restaurantes
    
    #total destinos
    restaurantes, destinos = ut.contar_tipos_nodos(my_graph)
    
    #promedio entrega de todos los domis
    total_tiempo = sum(total_tiempo)/len(total_tiempo)
                    
    tiempo_final = get_time()
    delta = delta_time(tiempo_inicial, tiempo_final)
    return catalog, total_domicilios, total_domiciliarios, total_nodos, total_arcos, restaurantes, destinos, total_tiempo, delta
    
    
    
# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Consulta en las Llamar la función del modelo para obtener un dato
    pass


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog, id_domiciliario,ubicacion_A,ubicacion_B):
    """
    Retorna el resultado del requerimiento 2
    """
    my_graph = catalog['domicilios']
    
    sub_grafo= gr.new_graph(1000)
    vertices = gr.vertices(my_graph)
    
    for v in vertices:
        
        info = gr.get_vertex_information(my_graph,v)
        if 'domiciliarios' in info and id_domiciliario in  info['domiciliarios']:
            gr.insert_vertex(sub_grafo,v,info)
            
    for v in gr.vertices(sub_grafo):
        
        info = gr.get_vertex_information(my_graph,v)
        
        if 'adjacents' in info:
            adjacents = info['adjacents']
            for w in mp.keys(adjacents):
                edge = mp.get(adjacents,w)
                
                destino_info = gr.get_vertex_information(my_graph,w)
                if id_domiciliario in destino_info.get('domiciliarios',[]):
                    gr.add_edge(sub_grafo,v,w,weight=edge['weight'],undirected=True)
                    
    # Recorrido BFS para encontrar el camino más corto
    
    visited = set()
    queue = deque()
    parent = {}
    
    queue.append(ubicacion_A)
    visited.add(ubicacion_A)
    parent[ubicacion_A] = None
    
    found = False
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


def req_7(catalog):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(catalog):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
