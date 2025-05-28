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
    files = data_dir + 'deliverytime_100.csv'
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
    total_arcos = (gr.size(my_graph))
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


def req_1(catalog, ubicacion_A, ubicacion_B):
    """
    Identifica si existe un camino simple entre dos ubicaciones geográficas usando DFS.
    Retorna tiempo de ejecución, cantidad de puntos, ids de domiciliarios, secuencia del camino y restaurantes encontrados.
    """
    tiempo_inicial = get_time()
    my_graph = catalog['domicilios']

    # DFS para encontrar un camino simple entre A y B
    stack = [(ubicacion_A, [ubicacion_A])]
    visited = set()
    path = []
    found = False

    while stack:
        current, current_path = stack.pop()
        if current == ubicacion_B:
            path = current_path
            found = True
            break
        if current not in visited:
            visited.add(current)
            try:
                adj_nodes = gr.adjacents(my_graph, current)
                for neighbor in adj_nodes['elements']:
                    if neighbor not in visited and neighbor not in current_path:
                        stack.append((neighbor, current_path + [neighbor]))
            except Exception:
                continue

    if not found:
        tiempo_final = get_time()
        return {
            'tiempo_en_ms': delta_time(tiempo_inicial, tiempo_final),
            'cantidad_puntos_geograficos': 0,
            'ids_domiciliarios': [],
            'camino': [],
            'restaurantes_en_camino': [],
            'mensaje': 'No existe un camino simple entre las ubicaciones.'
        }

    # Extraer ids de domiciliarios y restaurantes en el camino
    ids_domiciliarios = set()
    restaurantes = []
    for nodo in path:
        info = gr.get_vertex_information(my_graph, nodo)
        if 'info' in info:
            info = info['info']
        ids_domiciliarios.update(info.get('domiciliarios', []))
        if info.get('tipo') == 'restaurante':
            restaurantes.append(nodo)

    tiempo_final = get_time()
    return {
        'tiempo_en_ms': delta_time(tiempo_inicial, tiempo_final),
        'cantidad_puntos_geograficos': len(path),
        'ids_domiciliarios': list(ids_domiciliarios),
        'camino': path,
        'restaurantes_en_camino': restaurantes
    }


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
        


#catalogo = new_logic()

#load_data(catalogo)





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


#print(req_3(catalogo,'23.3646_77.5316'))


#print(gr.vertices(catalogo['domicilios']))


def req_4(catalog, ubicacion_A, ubicacion_B):
    """
    Identifica los domiciliarios en común entre los puntos geográficos A y B
    en el camino simple con menos puntos intermedios.
    """
    tiempo_inicial = get_time()
    my_graph = catalog['domicilios']

    # BFS para encontrar el camino más corto (menos puntos intermedios)
    bfs_result = bfs.bfs(my_graph, ubicacion_A)
    parent = bfs_result['parent']

    # Reconstruir el camino desde B hasta A
    path = []
    current = ubicacion_B
    while current is not None and current in parent:
        path.append(current)
        current = parent[current]
    path.reverse()

    # Si no hay camino, retornar mensaje
    if len(path) <= 1 or path[0] != ubicacion_A:
        tiempo_final = get_time()
        return {
            'tiempo_en_ms': delta_time(tiempo_inicial, tiempo_final),
            'camino': [],
            'domiciliarios_en_comun': [],
            'mensaje': 'No existe un camino simple entre las ubicaciones.'
        }

    # Encontrar domiciliarios en común en todos los nodos del camino
    domiciliarios_comunes = None
    for nodo in path:
        info = gr.get_vertex_information(my_graph, nodo)
        if 'info' in info:
            info = info['info']
        domis = set(info.get('domiciliarios', []))
        if domiciliarios_comunes is None:
            domiciliarios_comunes = domis
        else:
            domiciliarios_comunes = domiciliarios_comunes.intersection(domis)

    tiempo_final = get_time()
    return {
        'tiempo_en_ms': delta_time(tiempo_inicial, tiempo_final),
        'camino': path,
        'domiciliarios_en_comun': list(domiciliarios_comunes) if domiciliarios_comunes else []
    }


def req_5(catalog, ubicacion_A, N):
    """
    Identifica el domiciliario que recorre mayor cantidad de distancia en N cambios de ubicación geográfica a partir de un punto inicial.
    Retorna el tiempo de ejecución, el domiciliario (id y distancia en km) y la secuencia de ubicaciones del camino simple de mayor distancia.
    """
    tiempo_inicial = get_time()
    my_graph = catalog['domicilios']

    # Diccionario para guardar: {domiciliario: (distancia_total, [camino])}
    mejores_caminos = {}

    # Para cada domiciliario que pasa por el punto inicial
    info_inicio = gr.get_vertex_information(my_graph, ubicacion_A)
    if 'info' in info_inicio:
        info_inicio = info_inicio['info']
    domiciliarios = set(info_inicio.get('domiciliarios', []))

    for domi in domiciliarios:
        # Construir subgrafo solo para este domiciliario
        sub_grafo = gr.new_graph(1000)
        vertices = gr.vertices(my_graph)
        for v in vertices['elements']:
            info = gr.get_vertex_information(my_graph, v)
            if 'domiciliarios' in info['info'] and domi in info['info']['domiciliarios']:
                gr.insert_vertex(sub_grafo, v, info)
        for v in gr.vertices(sub_grafo)['elements']:
            info = gr.get_vertex_information(my_graph, v)
            if 'adjacents' in info:
                adjacents = info['adjacents']
                for w in mp.key_set(adjacents)['elements']:
                    if gr.contains_vertex(sub_grafo, w):
                        edge = mp.get(adjacents, w)
                        gr.add_edge(sub_grafo, v, w, weight=edge['weight'], undirected=True)

        # BFS para encontrar todos los caminos de longitud N desde ubicacion_A
        bfs_result = bfs.bfs(sub_grafo, ubicacion_A)
        parent = bfs_result['parent']

        # Buscar todos los nodos a distancia N desde ubicacion_A
        caminos = []
        for destino in gr.vertices(sub_grafo)['elements']:
            # Reconstruir camino desde destino hasta ubicacion_A
            path = []
            current = destino
            while current is not None and current in parent:
                path.append(current)
                current = parent[current]
            path.reverse()
            if len(path) == N + 1 and path[0] == ubicacion_A:
                caminos.append(path)

        # Calcular la distancia para cada camino y guardar el de mayor distancia
        max_dist = 0
        mejor_camino = []
        for path in caminos:
            dist = 0
            for i in range(len(path) - 1):
                info_v = gr.get_vertex_information(my_graph, path[i])
                info_w = gr.get_vertex_information(my_graph, path[i+1])
                lat1, lon1 = map(float, path[i].split('_'))
                lat2, lon2 = map(float, path[i+1].split('_'))
                dist += ut.haversine(lat1, lon1, lat2, lon2)
            if dist > max_dist:
                max_dist = dist
                mejor_camino = path

        if mejor_camino:
            mejores_caminos[domi] = (max_dist, mejor_camino)

    # Encontrar el domiciliario con mayor distancia
    if not mejores_caminos:
        tiempo_final = get_time()
        return {
            'tiempo_en_ms': delta_time(tiempo_inicial, tiempo_final),
            'mensaje': 'No se encontró ningún camino de longitud N desde el punto inicial.'
        }

    domi_max = max(mejores_caminos, key=lambda d: mejores_caminos[d][0])
    distancia_max, camino_max = mejores_caminos[domi_max]

    tiempo_final = get_time()
    return {
        'tiempo_en_ms': delta_time(tiempo_inicial, tiempo_final),
        'domiciliario': domi_max,
        'distancia_km': distancia_max,
        'camino': camino_max
    }


def req_6(catalog, ubicacion_A):
    """
    Identifica los caminos de costo mínimo en tiempo desde una ubicación geográfica específica.
    Retorna el tiempo de ejecución, cantidad de ubicaciones alcanzables, sus IDs ordenados, 
    y el camino de mayor tiempo mínimo desde el origen.
    """
    tiempo_inicial = get_time()
    my_graph = catalog['domicilios']

    # Ejecutar Dijkstra desde el nodo de inicio usando el peso 'weight' (tiempo)
    dijkstra_result = ut.dijkstra(my_graph, ubicacion_A)  # Debes tener una función dijkstra en utils

    # Extraer distancias y padres
    dist_to = dijkstra_result['dist_to']  # {nodo: tiempo_total}
    parent = dijkstra_result['parent']    # {nodo: predecesor}

    # Filtrar solo los nodos alcanzables (distancia < infinito)
    alcanzables = [nodo for nodo in dist_to if dist_to[nodo] < float('inf')]
    alcanzables.sort()  # Orden alfabético

    # Encontrar el nodo alcanzable con mayor tiempo mínimo
    if not alcanzables:
        tiempo_final = get_time()
        return {
            'tiempo_en_ms': delta_time(tiempo_inicial, tiempo_final),
            'cantidad_ubicaciones': 0,
            'ubicaciones_alcanzables': [],
            'camino_mayor_tiempo': [],
            'tiempo_total': 0,
            'mensaje': 'No hay ubicaciones alcanzables desde el punto dado.'
        }

    nodo_mayor_tiempo = max(alcanzables, key=lambda n: dist_to[n])
    tiempo_mayor = dist_to[nodo_mayor_tiempo]

    # Reconstruir el camino de costo mínimo a ese nodo
    camino = []
    current = nodo_mayor_tiempo
    while current is not None and current in parent:
        camino.append(current)
        current = parent[current]
    camino.reverse()

    tiempo_final = get_time()
    return {
        'tiempo_en_ms': delta_time(tiempo_inicial, tiempo_final),
        'cantidad_ubicaciones': len(alcanzables),
        'ubicaciones_alcanzables': alcanzables,
        'camino_mayor_tiempo': camino,
        'tiempo_total': tiempo_mayor
    }


def req_7(catalog, ubicacion_A, id_domiciliario):
    """
    Establece una subred (Árbol de Recubrimiento de Costo Mínimo en Tiempo) para un domiciliario particular desde una ubicación inicial.
    Retorna el tiempo de ejecución, cantidad de ubicaciones, IDs ordenados y el costo total en tiempo del árbol.
    """
    tiempo_inicial = get_time()
    my_graph = catalog['domicilios']

    # 1. Construir subgrafo solo con los nodos y aristas del domiciliario
    sub_grafo = gr.new_graph(1000)
    vertices = gr.vertices(my_graph)
    for v in vertices['elements']:
        info = gr.get_vertex_information(my_graph, v)
        if 'domiciliarios' in info['info'] and id_domiciliario in info['info']['domiciliarios']:
            gr.insert_vertex(sub_grafo, v, info)
    for v in gr.vertices(sub_grafo)['elements']:
        info = gr.get_vertex_information(my_graph, v)
        if 'adjacents' in info:
            adjacents = info['adjacents']
            for w in mp.key_set(adjacents)['elements']:
                if gr.contains_vertex(sub_grafo, w):
                    edge = mp.get(adjacents, w)
                    gr.add_edge(sub_grafo, v, w, weight=edge['weight'], undirected=True)

    # 2. Ejecutar Prim desde ubicacion_A en el subgrafo
    prim_result = ut.prim(sub_grafo, ubicacion_A)  # Debes tener una función prim en utils

    # 3. Extraer los nodos y el costo total del árbol
    mst_edges = prim_result['mst_edges']  # Lista de aristas [(u, v, peso)]
    mst_vertices = set()
    total_tiempo = 0
    for u, v, peso in mst_edges:
        mst_vertices.add(u)
        mst_vertices.add(v)
        total_tiempo += peso

    ubicaciones = sorted(list(mst_vertices))

    tiempo_final = get_time()
    return {
        'tiempo_en_ms': delta_time(tiempo_inicial, tiempo_final),
        'cantidad_ubicaciones': len(ubicaciones),
        'ubicaciones_subred': ubicaciones,
        'tiempo_total': total_tiempo
    }


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
