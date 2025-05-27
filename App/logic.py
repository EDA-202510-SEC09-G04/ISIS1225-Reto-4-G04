from dis import dis
import time
import os
import csv
import sys
import math
import pprint as pprint
from datetime import datetime
from DataStructures.Map import map_separate_chaining as msc
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as slist
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf
from DataStructures.Utils import error as error
from DataStructures.Graph import digraph as gr
from DataStructures.Map import map_linear_probing as mp
from collections import deque


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


#formateo id del nodo
def format_coord(coord):
    coord = float(coord)
    integer_part, decimal_part = str(coord).split('.')
    formatted_decimal = (decimal_part + '0000')[:4]
    return f"{integer_part}.{formatted_decimal}"

def format_location(lat, lon):
    formatted_lat = format_coord(lat)
    formatted_lon = format_coord(lon)
    return f"{formatted_lat}_{formatted_lon}"

    
def calcular_peso(my_graph, origen, destino):
    info = gr.get_vertex_information(my_graph, origen)
    if 'tiempos' not in info or destino not in info['tiempos']:
        return 0  # Valor por defecto
    
    tiempos = info['tiempos'][destino]
    if not tiempos:
        return 0
        
    return sum(tiempos) // len(tiempos)

    
def contar_tipos_nodos(my_graph):
    vertices = gr.vertices(my_graph)
    num_restaurantes = 0
    num_destinos = 0

    for key in vertices:
        info = mp.get(my_graph['vertices'], key)
        tipo = info.get('tipo')
        if tipo == 'restaurante':
            num_restaurantes += 1
        elif tipo == 'destino':
            num_destinos += 1

    return num_restaurantes, num_destinos


def load_data(catalog):
    """
    Carga los datos del reto
    """
    tiempo_inicial = get_time()
    files = data_dir + 'deliverytime_40.csv'
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
        id_rest = format_location(rest_lat, rest_lon) 
        id_des = format_location(des_lat, des_lon) 
        
        #obtener id del domiciliario
        id_domiciliario = row['Delivery_person_ID']
        
        
        #obtener tiempo tomado del domicilio
        time = row['Time_taken(min)']
        total_tiempo.append(int(time))
    
        #creacion de los dos nodos
        def crear_nodo(my_graph, origen, destino, id_domiciliario, time, tipo):
            time_int = int(time)
            if not gr.contains_vertex(my_graph, origen):
                # Crear nuevo nodo
                new_vertex = {
                    'domiciliarios': [id_domiciliario],
                    'tiempos': {destino: [time_int]},
                    'tipo': tipo
                }
                gr.insert_vertex(my_graph, origen, new_vertex)
            else:
                # Actualizar nodo existente
                info = gr.get_vertex_information(my_graph, origen)
                
                # 1. Actualizar lista de domiciliarios (sin duplicados)
                if 'domiciliarios' not in info:
                    info['domiciliarios'] = []
                if id_domiciliario not in info['domiciliarios']:
                    info['domiciliarios'].append(id_domiciliario)
                
                # 2. Actualizar tiempos (manteniendo historial)
                if 'tiempos' not in info:
                    info['tiempos'] = {}
                if destino not in info['tiempos']:
                    info['tiempos'][destino] = []
                info['tiempos'][destino].append(time_int)
                
                # 3. Conservar el tipo (por si acaso)
                info['tipo'] = tipo
                
                # Actualizar el vértice en el grafo
                gr.update_vertex_info(my_graph, origen, info)
       
        #creacion nodo del origen con lista de domiciliarios
        crear_nodo(my_graph, id_rest, id_des, id_domiciliario, time, 'restaurante')
        #creacion nodo del destino con  lista de domiciliarios
        crear_nodo(my_graph, id_des, id_rest, id_domiciliario, time, 'destino')
        
    
        
        #CREACION DE ARCOS

        #crear arco entre origen y destino
        if not gr.has_edge(my_graph, id_rest, id_des):
            peso = calcular_peso(my_graph, id_rest, id_des)
            gr.add_edge(my_graph, id_rest, id_des, weight=peso, undirected=True)
        else: 
            # actualizar el peso del arco en ambas direcciones
            nuevo_peso = calcular_peso(my_graph, id_rest, id_des)
            
            # actualizar u → v
            u_entry = mp.get(my_graph['vertices'], id_rest)
            if u_entry and 'adjacents' in u_entry:
                # Aquí está el cambio importante - usar mp.put correctamente
                edge_info = {'to': id_des, 'weight': nuevo_peso}
                u_entry['adjacents'] = mp.put(u_entry['adjacents'], id_des, edge_info)
            
            # actualizar v → u si es no dirigido
            v_entry = mp.get(my_graph['vertices'], id_des)
            if v_entry and 'adjacents' in v_entry:
                edge_info = {'to': id_rest, 'weight': nuevo_peso}
                v_entry['adjacents'] = mp.put(v_entry['adjacents'], id_rest, edge_info)

        
        # HISTORIAL DE DOMICILIARIOS
        if id_domiciliario not in historial:
            historial[id_domiciliario] = []

        # Añadir el nuevo pedido al historial si no está
        if (id_rest, id_des) not in historial[id_domiciliario]:
            historial[id_domiciliario].append((id_rest, id_des))

            # Si hay un pedido anterior
            if len(historial[id_domiciliario]) >= 2:
                anterior = historial[id_domiciliario][-2]
                actual = historial[id_domiciliario][-1]

                nodo_anterior = anterior[1]  # destino del pedido anterior
                nodo_actual = actual[1]      # destino del pedido actual

                # calcular los tiempos actualizados usando la función que ya tienes
                tiempo_anterior = calcular_peso(my_graph, anterior[0], anterior[1])
                tiempo_actual = calcular_peso(my_graph, actual[0], actual[1])
                promedio = (tiempo_anterior + tiempo_actual) / 2

                # crear o actualizar arco entre destinos
                if not gr.has_edge(my_graph, nodo_anterior, nodo_actual):
                    gr.add_edge(my_graph, nodo_anterior, nodo_actual, weight=promedio, undirected=True)
                else:
                    #si ya existe el arco pero hay que actualizar los pesos
                    #actualizar en el nodo origen
                    origen_entry = mp.get(my_graph['vertices'], nodo_anterior)

                    if 'adjacents' in origen_entry and mp.contains(origen_entry['adjacents'], nodo_actual):
                        # Actualizar el peso del arco sin aumentar el contador de aristas
                        edge_info = {'to': nodo_actual, 'weight': promedio}
                        mp.put(origen_entry['adjacents'], nodo_actual, edge_info)
                        

                    #actualizar en el nodo destino
                    destino_entry = mp.get(my_graph['vertices'], nodo_actual)
                    
                    if 'adjacents' in destino_entry and mp.contains(destino_entry['adjacents'], nodo_anterior):
                        edge_info = {'to': nodo_anterior, 'weight': promedio}
                        mp.put(destino_entry['adjacents'], nodo_anterior, edge_info)

    print("Grafo creado.")
    
    #RETORNOS AL FINAL
    #domicilios procesados
    #domiciliarios identificados
    total_domiciliarios = len(historial)
    #total nodos
    total_nodos = gr.order(my_graph)
    #total arcos
    total_arcos = gr.size(my_graph)
    #total restaurantes
    #total destinos
    restaurantes, destinos = contar_tipos_nodos(my_graph)
    
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
