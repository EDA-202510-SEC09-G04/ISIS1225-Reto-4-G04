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
from DataStructures.Graph import bfs as bfs
from DataStructures.Map import map_linear_probing as mp
from App import utils as ut

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'

defualt_limit = 1000
sys.setrecursionlimit(defualt_limit*10)
csv.field_size_limit(2147483647)



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
    
    tiempo_inicial = get_time()
    my_graph = catalog['domicilios']
    
    sub_grafo= gr.new_graph(1000)
    vertices = gr.vertices(my_graph)
   # print(vertices)
    for v in vertices['elements']:
        
         info = gr.get_vertex_information(my_graph,v)
         if 'domiciliarios' in info['info'] and id_domiciliario in  info['info']['domiciliarios']:
            gr.insert_vertex(sub_grafo,v,info)
            
    for v in gr.vertices(sub_grafo)['elements']:
       
         info = gr.get_vertex_information(my_graph,v)
        
        
         
         if 'adjacents' in info:
            adjacents = info['adjacents']
          
            
            for w in mp.key_set(adjacents)['elements']:
                
                destino_info = gr.get_vertex_information(my_graph,w)
                
                if id_domiciliario in destino_info['info']['domiciliarios']:
                    edge = mp.get(adjacents, w)
                    
                    if  v is not None and w is not None and gr.contains_vertex(sub_grafo, v) and gr.contains_vertex(sub_grafo, w):
                         gr.add_edge(sub_grafo, v, w, weight=edge['weight'], undirected=True)
                    
                    
    # Recorrido BFS para encontrar el camino más corto
    bfs_result = bfs.bfs(sub_grafo,ubicacion_A)
    parent = bfs_result['parent']
    
    path = []
    current = ubicacion_B
    while current is not None and current in parent:
        path.append(current)
        current = parent[current]
       
        
    path.reverse()
    
    print(path)
    if len(path) > 1 and path[0] == ubicacion_A:
        
        ids_domiciliarios = [id_domiciliario]
        restaurantes = []

        
        for nodo in path:
            
            info = gr.get_vertex_information(my_graph,nodo)
            
            if info.get('tipo') == 'restaurante':
                restaurantes.append(nodo)
                
        respuesta = {
            
            'cantidad_puntos_geograficos': len(path),
            'ids_domiciliarios': ids_domiciliarios,
            'camino': path,
            'restaurantes_en_camino': restaurantes
        }       
        
    else:
        
        respuesta = {
            
            'cantidad_puntos_geograficos': 0,
            'ids_domiciliarios': [],
            'camino': [],
            'restaurantes_en_camino': [],
            'mensaje': 'No existe un camino simple entre las ubicaciones para ese domiciliario.'
        }
        
    
    tiempo_final = get_time()
    
    delta_time = tiempo_final - tiempo_inicial
    
    respuesta['tiempo_en_ms'] = delta_time
    
    return respuesta
        


catalogo = new_logic()

load_data(catalogo)





#print(req_2(catalogo,'INDORES16DEL02',ut.format_location('22.744648','75.894377'),ut.format_location('22.310237','73.158921')))

        
def req_3(catalog, punto_geografico):
    """
    Identifica el domiciliario con mayor cantidad de pedidos para un punto geográfico específico.
    Retorna el tiempo de ejecución, el domiciliario más popular, la cantidad de pedidos y el tipo de vehículo más usado por ese domiciliario en ese punto.
    """
    tiempo_inicial = get_time()
    my_graph = catalog['domicilios']

    if not gr.contains_vertex(my_graph, punto_geografico):
        return {
            'mensaje': 'El punto geográfico no existe en el grafo.',
            'tiempo_en_ms': 0
        }

    info = gr.get_vertex_information(my_graph, punto_geografico)
    # info['info'] si tu estructura es anidada
    if 'info' in info:
        info = info['info']

    # Contar pedidos por domiciliario y tipos de vehículo
    contador_domi = {}
    vehiculos_domi = {}

    if 'domiciliarios' in info:
        for domi in info['domiciliarios']:
            if domi not in contador_domi:
                contador_domi[domi] = 0
                vehiculos_domi[domi] = {}
            contador_domi[domi] += 1
            # Contar tipo de vehículo si está disponible
            if 'vehiculos' in info:
                vehiculo = info['vehiculos'].get(domi)
                if vehiculo:
                    vehiculos_domi[domi][vehiculo] = vehiculos_domi[domi].get(vehiculo, 0) + 1

    if not contador_domi:
        return {
            'mensaje': 'No hay pedidos en ese punto geográfico.',
            'tiempo_en_ms': delta_time(tiempo_inicial, get_time())
        }

    # Encontrar domiciliario con más pedidos
    domi_popular = max(contador_domi, key=contador_domi.get)
    cantidad_pedidos = contador_domi[domi_popular]

    # Tipo de vehículo más usado por ese domiciliario
    tipo_vehiculo = None
    if domi_popular in vehiculos_domi and vehiculos_domi[domi_popular]:
        tipo_vehiculo = max(vehiculos_domi[domi_popular], key=vehiculos_domi[domi_popular].get)

    tiempo_final = get_time()
    return {
        'tiempo_en_ms': delta_time(tiempo_inicial, tiempo_final),
        'domiciliario_mas_popular': domi_popular,
        'cantidad_pedidos': cantidad_pedidos,
        'vehiculo_mas_usado': tipo_vehiculo
    }


print(req_3(catalogo,'23.359407_85.325055'))


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
