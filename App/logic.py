import os
import csv
import math
from time import time
from DataStructures.Map import map_linear_probing as map
from DataStructures.Graph import digraph as g 
from DataStructures.List import array_list as lt
from DataStructures.Graph import dfs
from DataStructures.Graph import bfs
from DataStructures.Graph import dijkstra as dijk
from DataStructures.Graph import prim 
import folium
from App import bono
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'


def new_catalog():
    
    catalog = {
        'grafo_domicilios': None,
        'ultimo_domicilio_persona': None,
        'ubicaciones_procesadas': None,
        'promedio_arcos_grafo': None,
        'ubicaciones_restaurantes_unicas': None, # Mapa para contar ubicaciones de origen únicas
        'ubicaciones_destino_unicas': None
    }
    catalog['grafo_domicilios'] = g.new_graph(100000) 
    catalog['ultimo_domicilio_persona'] = map.new_map(100000,0.5)
    catalog['ubicaciones_procesadas'] = map.new_map(100000, 0.5) 
    catalog['promedio_arcos_grafo'] = map.new_map(200000, 0.5) 
    catalog['ubicaciones_restaurantes_unicas'] = map.new_map(200000, 0.5)
    catalog['ubicaciones_destino_unicas'] = map.new_map(200000, 0.5)
                #PARA REQ 3
            
    catalog['pedidos_por_ubicacion_persona']   = map.new_map(500000, 0.5)
    catalog['vehiculos_por_ubicacion_persona'] = map.new_map(500000, 0.5)
     

    return catalog

def formatear_cordenada(coord_value):
    scale = 10**4 
    truncated_value = math.trunc(coord_value * scale) / scale
    return f"{truncated_value:.4f}"

def load_data(catalog, filename):
    total_domicilios_procesados = 0
    total_tiempo_entregas = 0
    filepath = data_dir + filename
    
    with open(filepath, encoding="utf-8") as csvfile:
        input_reader = csv.DictReader(csvfile, delimiter=",")
        
        for pedido in input_reader:
            limpio = {
                'ID': pedido['ID'],
                'Delivery_person_ID': pedido['Delivery_person_ID'],
                'Delivery_person_Age': int(pedido['Delivery_person_Age']),
                'Delivery_person_Ratings': float(pedido['Delivery_person_Ratings']),
                'Restaurant_latitude_float': float(pedido['Restaurant_latitude']),
                'Restaurant_longitude_float': float(pedido['Restaurant_longitude']),
                'Delivery_location_latitude_float': float(pedido['Delivery_location_latitude']),
                'Delivery_location_longitude_float': float(pedido['Delivery_location_longitude']),
                'Type_of_order': pedido['Type_of_order'],
                'Type_of_vehicle': pedido['Type_of_vehicle'],
                'Time_taken': float(pedido['Time_taken(min)'])
            }
            total_domicilios_procesados += 1
            total_tiempo_entregas += limpio['Time_taken']
            id_origen = formatear_cordenada(limpio['Restaurant_latitude_float']) + '_' + formatear_cordenada(limpio['Restaurant_longitude_float'])
            id_destino = formatear_cordenada(limpio['Delivery_location_latitude_float']) + '_' + formatear_cordenada(limpio['Delivery_location_longitude_float'])
            
            dp = limpio['Delivery_person_ID']
            vt = limpio['Type_of_vehicle']
            _acumular_req3(catalog, id_origen, dp, vt)
            _acumular_req3(catalog, id_destino,  dp, vt)


            map.put(catalog['ubicaciones_restaurantes_unicas'], id_origen, True) 
            map.put(catalog['ubicaciones_destino_unicas'], id_destino, True) 
            


            add_pedido_connection(
                catalog, 
                limpio['Restaurant_latitude_float'],
                limpio['Restaurant_longitude_float'],
                limpio['Delivery_location_latitude_float'],
                limpio['Delivery_location_longitude_float'],
                limpio['Time_taken'],
                limpio['Delivery_person_ID']
            )
    
    
    return catalog, total_domicilios_procesados, total_tiempo_entregas


def add_pedido_connection(catalog,
                         rest_lat_f, rest_lon_f,
                         del_lat_f, del_lon_f,
                         time_taken, delivery_person_id):


    #Formatear coordenadas  a IDs de nodo (en string)
    id_origen = formatear_cordenada(rest_lat_f) + '_' + formatear_cordenada(rest_lon_f)
    id_destino = formatear_cordenada(del_lat_f) + '_' + formatear_cordenada(del_lon_f)

    # Añadir o Actualizar Nodos en el Grafo (y sus listas de domiciliarios con los ids)
    add_node_with_delivery_person(catalog, id_origen, delivery_person_id)
    add_node_with_delivery_person(catalog, id_destino, delivery_person_id)

    # Añadir Arco No Dirigido entre Origen y Destino del Pedido
    canonical_edge_key_pedido = tuple(sorted((id_origen, id_destino)))
    
    current_edge_data = map.get(catalog['promedio_arcos_grafo'], canonical_edge_key_pedido)
    
    if current_edge_data is None:
        map.put(catalog['promedio_arcos_grafo'], canonical_edge_key_pedido, {'total_time': time_taken, 'count': 1})
        final_edge_weight_pedido = time_taken
    else:
        current_edge_data['total_time'] += time_taken
        current_edge_data['count'] += 1
        map.put(catalog['promedio_arcos_grafo'], canonical_edge_key_pedido, current_edge_data)
        final_edge_weight_pedido = current_edge_data['total_time'] / current_edge_data['count']
    
    g.add_edge(catalog['grafo_domicilios'], id_origen, id_destino, final_edge_weight_pedido)


    # añadir Arco Adicional desde destino Actual a el destino Anterior del mismo domiciliario
    info_last_delivery = map.get(catalog['ultimo_domicilio_persona'], delivery_person_id)

    if info_last_delivery is not None:
        last_del_location_id = info_last_delivery['last_delivery_location_id']
        last_del_time = info_last_delivery['last_delivery_time']

        if last_del_location_id != id_destino:
            avg_time_between_deliveries = (time_taken + last_del_time) / 2.0
            canonical_edge_key_delivery_chain = tuple(sorted((id_destino, last_del_location_id)))

            current_chain_edge_data = map.get(catalog['promedio_arcos_grafo'], canonical_edge_key_delivery_chain)

            if current_chain_edge_data is None:
                map.put(catalog['promedio_arcos_grafo'], canonical_edge_key_delivery_chain, {'total_time': avg_time_between_deliveries, 'count': 1})
                final_chain_edge_weight = avg_time_between_deliveries
            else:
                current_chain_edge_data['total_time'] += avg_time_between_deliveries
                current_chain_edge_data['count'] += 1
                map.put(catalog['promedio_arcos_grafo'], canonical_edge_key_delivery_chain, current_chain_edge_data)
                final_chain_edge_weight = current_chain_edge_data['total_time'] / current_chain_edge_data['count']
            
            g.add_edge(catalog['grafo_domicilios'], id_destino, last_del_location_id, final_chain_edge_weight)
    
    map.put(catalog['ultimo_domicilio_persona'], delivery_person_id, {
        'last_delivery_location_id': id_destino,
        'last_delivery_time': time_taken
    })

    return catalog


def add_node_with_delivery_person(catalog, node_id, delivery_person_id):

    list_of_delivery_persons_for_node = map.get(catalog['ubicaciones_procesadas'], node_id)
    
    if list_of_delivery_persons_for_node is None:
        new_list_for_node = lt.new_list() 
        lt.add_last(new_list_for_node, delivery_person_id) 

        g.insert_vertex(catalog['grafo_domicilios'], node_id, new_list_for_node)
        map.put(catalog['ubicaciones_procesadas'], node_id, new_list_for_node)
        
    else:
        id_already_in_list = False
        for i in range(lt.size(list_of_delivery_persons_for_node)):
            if lt.get_element(list_of_delivery_persons_for_node, i) == delivery_person_id:
                id_already_in_list = True
                break
        
        if not id_already_in_list:
            lt.add_last(list_of_delivery_persons_for_node, delivery_person_id)
            g.update_vertex_info(catalog['grafo_domicilios'], node_id, list_of_delivery_persons_for_node)
            

            
def _acumular_req3(catalog, nodo_id, dp, vt):
    """
    Actualiza en el catálogo para Req.3:
      - contador de pedidos en (nodo_id, dp)
      - contador de tipo de vehículo vt en (nodo_id, dp)
    """
    key_lp = (nodo_id, dp)

    # 1) Incrementar contador de pedidos
    prev = map.get(catalog['pedidos_por_ubicacion_persona'], key_lp) or 0
    map.put(catalog['pedidos_por_ubicacion_persona'], key_lp, prev + 1)

    # 2) Incrementar contador de vehículo
    veh_map = map.get(catalog['vehiculos_por_ubicacion_persona'], key_lp)
    if veh_map is None:
        veh_map = map.new_map(10, 0.5)
    prev_v = map.get(veh_map, vt) or 0
    map.put(veh_map, vt, prev_v + 1)
    map.put(catalog['vehiculos_por_ubicacion_persona'], key_lp, veh_map)

            
# Funciones de consulta sobre el catálogo


def req_1(catalog,ubicacion_A,ubicacion_B):
    mapa_dfs = dfs.dfs(catalog['grafo_domicilios'],ubicacion_A)
    conexion = map.key_set(mapa_dfs['visited'])
    if ubicacion_B in conexion['elements']:
        return mapa_dfs, catalog['grafo_domicilios']
    else: 
        return None
        

def crear_subgrafo_para_domiciliario(grafo_original, domiciliario_id_filtro):
    subgrafo = g.new_graph(g.order(grafo_original), directed=False) 
    nodos_en_subgrafo = map.new_map(g.order(grafo_original), 0.5)
    #Identificar y añadir vértices al subgrafo que contengan al domiciliario
    claves_vertices_originales = g.vertices(grafo_original) 
    for i in range(lt.size(claves_vertices_originales)):
        clave_vertice = lt.get_element(claves_vertices_originales, i)
        lista_domiciliarios_nodo = g.get_vertex_info(grafo_original, clave_vertice)
        domiciliario_encontrado_en_nodo = False
        if lista_domiciliarios_nodo is not None:
            for k in range(lt.size(lista_domiciliarios_nodo)):
                if lt.get_element(lista_domiciliarios_nodo, k) == domiciliario_id_filtro:
                    domiciliario_encontrado_en_nodo = True
                    break
        if domiciliario_encontrado_en_nodo:
            g.insert_vertex(subgrafo, clave_vertice, lista_domiciliarios_nodo)
            map.put(nodos_en_subgrafo, clave_vertice, True) 
    claves_vertices_subgrafo = map.key_set(nodos_en_subgrafo) # llaves de los nodos que están en el subgrafo
    for i in range(lt.size(claves_vertices_subgrafo)):
        clave_u = lt.get_element(claves_vertices_subgrafo, i)
        # Obtener los adyacentes de 'u' en el grafo ORIGINAL (para ver las aristas)
        adyacentes_u_original = g.adjacents(grafo_original, clave_u) # Esto devuelve array_list de llaves
        if adyacentes_u_original is not None:
            for j in range(lt.size(adyacentes_u_original)):
                clave_v = lt.get_element(adyacentes_u_original, j)
                # Verificar si el vecino 'v' también está en el subgrafo
                if map.get(nodos_en_subgrafo, clave_v) is not None:
                    mapa_adyacencia_u_original = g.get_adjacents(grafo_original, clave_u) # Esto devuelve un mapa
                    arista_original = map.get(mapa_adyacencia_u_original, clave_v)
                    peso_arista = arista_original['weight']
                    g.add_edge(subgrafo, clave_u, clave_v, peso_arista)

    return subgrafo  
    
def req_2 (catalog, punto_a, punto_b, domiciliario ):
    #1. Crear el subgrafo de los nodos que contiendes el domiciliario.
    subgrafo = crear_subgrafo_para_domiciliario(catalog['grafo_domicilios'],domiciliario)
    mapa_bfs = bfs.bfs(subgrafo,punto_a)
    conexion = map.key_set(mapa_bfs['visited'])
    if punto_b in conexion['elements']:
        return mapa_bfs, catalog["grafo_domicilios"]
    else: 
        return None 
    

def req_3(catalog, geo_point_a):

    # 1) Buscar domiciliario con más pedidos en geo_point_a
    domic_maximo_id = None
    pedidos_maximos = 0
    llaves = map.key_set(catalog['pedidos_por_ubicacion_persona'])
    for i in range(lt.size(llaves)):
        ubicacion, dp_id = lt.get_element(llaves, i)
        if ubicacion == geo_point_a:
            cantidad = map.get(catalog['pedidos_por_ubicacion_persona'], (ubicacion, dp_id))
            if cantidad > pedidos_maximos:
                pedidos_maximos, domic_maximo_id = cantidad, dp_id

    # 2) Si no hay pedidos
    if domic_maximo_id is None:
        return None, 0, None

    # 3) Vehículo más usado por ese domiciliario en ese punto
    vehiculo_favorito = None
    contador_vehiculo_max = 0
    mapa_veh = map.get(catalog['vehiculos_por_ubicacion_persona'], (geo_point_a, domic_maximo_id))
    if mapa_veh is not None:
        llaves_v = map.key_set(mapa_veh)
        for j in range(lt.size(llaves_v)):
            veh = lt.get_element(llaves_v, j)
            uso = map.get(mapa_veh, veh)
            if uso > contador_vehiculo_max:
                contador_vehiculo_max, vehiculo_favorito = uso, veh

    return domic_maximo_id, pedidos_maximos, vehiculo_favorito







def req_4(catalog, punto_a, punto_b): 

    if g.get_vertex_info(catalog['grafo_domicilios'], punto_a) is None: 
        return (lt.new_list(), lt.new_list(), False)
    if g.get_vertex_info(catalog['grafo_domicilios'], punto_b) is None: 
        return (lt.new_list(), lt.new_list(), False)

    resultados_bfs = bfs.bfs(catalog['grafo_domicilios'], punto_a) 
    secuencia_camino = bfs.pathTo(resultados_bfs, punto_b) 
    # Si no hay camino a la ubicación final
    if secuencia_camino is None:
        return (lt.new_list(), lt.new_list(), False)
    id_primer_nodo = lt.get_element(secuencia_camino, 0)
    domiciliarios_primer_nodo = g.get_vertex_info(catalog['grafo_domicilios'], id_primer_nodo) 
    
    if domiciliarios_primer_nodo is None:
        lista_domiciliarios_comunes = lt.new_list() 
    else:
        lista_domiciliarios_comunes = lt.new_list()
        for i in range(lt.size(domiciliarios_primer_nodo)):
            lt.add_last(lista_domiciliarios_comunes, lt.get_element(domiciliarios_primer_nodo, i))
            
    #  resto de los nodos del camino (desde el segundo nodo en adelante)
    indice_nodo_camino = 1 
    
    while indice_nodo_camino < lt.size(secuencia_camino) and not lt.is_empty(lista_domiciliarios_comunes):
        id_nodo_actual = lt.get_element(secuencia_camino, indice_nodo_camino)
        domiciliarios_nodo_actual = g.get_vertex_info(catalog['grafo_domicilios'], id_nodo_actual)
        
        if domiciliarios_nodo_actual is None:
            lista_domiciliarios_comunes = lt.new_list() 
        else:
            siguientes_candidatos_comunes = lt.new_list()
            
            indice_busqueda_dom = 0
            while indice_busqueda_dom < lt.size(lista_domiciliarios_comunes):
                domiciliario_candidato = lt.get_element(lista_domiciliarios_comunes, indice_busqueda_dom)
                
                encontrado_en_nodo_actual = False
                indice_en_nodo_actual = 0
                while indice_en_nodo_actual < lt.size(domiciliarios_nodo_actual) and not encontrado_en_nodo_actual:
                    if lt.get_element(domiciliarios_nodo_actual, indice_en_nodo_actual) == domiciliario_candidato:
                        encontrado_en_nodo_actual = True
                    indice_en_nodo_actual += 1 
                
                if encontrado_en_nodo_actual:
                    lt.add_last(siguientes_candidatos_comunes, domiciliario_candidato)
                indice_busqueda_dom += 1 
            lista_domiciliarios_comunes = siguientes_candidatos_comunes
        indice_nodo_camino += 1 
        
    return secuencia_camino, lista_domiciliarios_comunes


def _haversine(a_lat, a_lon, b_lat, b_lon):
    R = 6371.0
    phi1 = math.radians(a_lat)
    phi2 = math.radians(b_lat)
    delta_phi = math.radians(b_lat - a_lat)
    delta_lambda = math.radians(b_lon - a_lon)
    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def req_5(catalog, punto_inicial_id, N_cambios):
    start_time = time()

    domiciliario_max_distancia_global = None
    max_distancia_global = -1.0
    camino_optimo_global = lt.new_list()

    grafo = catalog['grafo_domicilios']

    if g.get_vertex_info(grafo, punto_inicial_id) is None:
        return None, 0.0, lt.new_list(), (time() - start_time)

    
    memo_dfs_estados = {}


    def _explorar_dfs(nodo_actual_id, n_restantes, camino_parcial_nodos_actual, dist_parcial_km_actual, domiciliarios_comunes_camino_actual, visitados_en_camino_actual):
        nonlocal domiciliario_max_distancia_global, max_distancia_global, camino_optimo_global
        
        estado_actual = (nodo_actual_id, n_restantes, tuple(lt.to_list(domiciliarios_comunes_camino_actual)), tuple(sorted(lt.to_list(visitados_en_camino_actual))))
        if estado_actual in memo_dfs_estados and memo_dfs_estados[estado_actual] >= dist_parcial_km_actual:
            return
        memo_dfs_estados[estado_actual] = dist_parcial_km_actual
        
        lt.add_last(camino_parcial_nodos_actual, nodo_actual_id)
        lt.add_last(visitados_en_camino_actual, nodo_actual_id)

        if n_restantes == 0:
            if not lt.is_empty(domiciliarios_comunes_camino_actual):
                for i in range(lt.size(domiciliarios_comunes_camino_actual)):
                    dom_actual = lt.get_element(domiciliarios_comunes_camino_actual, i)
                    if dist_parcial_km_actual > max_distancia_global:
                        max_distancia_global = dist_parcial_km_actual
                        domiciliario_max_distancia_global = dom_actual
                        camino_optimo_global = lt.new_list()
                        for j in range(lt.size(camino_parcial_nodos_actual)):
                            lt.add_last(camino_optimo_global, lt.get_element(camino_parcial_nodos_actual,j))
            
            lt.remove_last(visitados_en_camino_actual)
            lt.remove_last(camino_parcial_nodos_actual)
            return

        adyacentes_ids = g.adjacents(grafo, nodo_actual_id)

        if adyacentes_ids is not None:
            for i in range(lt.size(adyacentes_ids)):
                vecino_id = lt.get_element(adyacentes_ids, i)
                
                vecino_ya_visitado_en_este_camino = False
                for k_visitado in range(lt.size(visitados_en_camino_actual)):
                    if lt.get_element(visitados_en_camino_actual, k_visitado) == vecino_id:
                        vecino_ya_visitado_en_este_camino = True
                        break
                if vecino_ya_visitado_en_este_camino: # Para camino simple
                    continue


                try:
                    lat_actual_str, lon_actual_str = nodo_actual_id.split('_')
                    lat_vecino_str, lon_vecino_str = vecino_id.split('_')
                    
                    lat_actual, lon_actual = float(lat_actual_str), float(lon_actual_str)
                    lat_vecino, lon_vecino = float(lon_vecino_str), float(lon_vecino_str)
                except ValueError:
                    continue

                distancia_arco = _haversine(lat_actual, lon_actual, lat_vecino, lon_vecino)
                
                domiciliarios_vecino_info = g.get_vertex_info(grafo, vecino_id)
                if domiciliarios_vecino_info is None or lt.is_empty(domiciliarios_vecino_info):
                    continue

                nuevos_domiciliarios_comunes_para_rama = lt.new_list()
                for k_dom_camino in range(lt.size(domiciliarios_comunes_camino_actual)):
                    dom_c = lt.get_element(domiciliarios_comunes_camino_actual, k_dom_camino)
                    encontrado_en_vecino = False
                    for k_dom_vecino in range(lt.size(domiciliarios_vecino_info)):
                        if dom_c == lt.get_element(domiciliarios_vecino_info, k_dom_vecino):
                            encontrado_en_vecino = True
                            break
                    if encontrado_en_vecino:
                         lt.add_last(nuevos_domiciliarios_comunes_para_rama, dom_c)
                
                if not lt.is_empty(nuevos_domiciliarios_comunes_para_rama):
                    _explorar_dfs(vecino_id, n_restantes - 1, camino_parcial_nodos_actual, dist_parcial_km_actual + distancia_arco, nuevos_domiciliarios_comunes_para_rama, visitados_en_camino_actual)
        
        lt.remove_last(visitados_en_camino_actual)
        lt.remove_last(camino_parcial_nodos_actual)

    domiciliarios_iniciales = g.get_vertex_info(grafo, punto_inicial_id)
    if domiciliarios_iniciales is None or lt.is_empty(domiciliarios_iniciales):
        return None, 0.0, lt.new_list(), (time() - start_time)

    camino_inicial_nodos_lista = lt.new_list()
    visitados_inicial_lista = lt.new_list() 
    
    
    domiciliarios_iniciales_copia = lt.new_list()
    for i in range(lt.size(domiciliarios_iniciales)):
        lt.add_last(domiciliarios_iniciales_copia, lt.get_element(domiciliarios_iniciales,i))

    _explorar_dfs(punto_inicial_id, N_cambios, camino_inicial_nodos_lista, 0.0, domiciliarios_iniciales_copia, visitados_inicial_lista)
    
    duracion = time() - start_time
    
    if domiciliario_max_distancia_global is None:
            return None, 0.0, lt.new_list(), duracion

    return domiciliario_max_distancia_global, max_distancia_global, camino_optimo_global, duracion

def req_6(catalog, punto_a):
    costo_min = dijk.dijkstra(catalog['grafo_domicilios'],punto_a)
    ubicaciones_alcanzables_list_py = [] 
    max_tiempo_alcanzable = -1.0 
    ubicacion_mayor_tiempo = None
    all_vertices_keys_lt = g.vertices(catalog['grafo_domicilios']) 
    for i in range(lt.size(all_vertices_keys_lt)):
        v_key = lt.get_element(all_vertices_keys_lt, i) 
        if dijk.has_path_to(v_key, costo_min):
            ubicaciones_alcanzables_list_py.append(v_key) 
            current_dist = dijk.dist_to(v_key, costo_min)
            if current_dist > max_tiempo_alcanzable:
                max_tiempo_alcanzable = current_dist
                ubicacion_mayor_tiempo = v_key
                
    ubicaciones_alcanzables_list_py.sort() 
    identificadores_alcanzables_ordenados_lt = lt.new_list()
    for id_val in ubicaciones_alcanzables_list_py:
        lt.add_last(identificadores_alcanzables_ordenados_lt, id_val)
        
    secuencia_camino_mayor_tiempo_lt = lt.new_list() 
    if ubicacion_mayor_tiempo is not None:
        secuencia_camino_mayor_tiempo_lt = dijk.path_to(ubicacion_mayor_tiempo, costo_min)
    
    
    return len(ubicaciones_alcanzables_list_py), identificadores_alcanzables_ordenados_lt, secuencia_camino_mayor_tiempo_lt, max_tiempo_alcanzable
    
            
        
def crear_subgrafo_para_domiciliario(grafo_original, domiciliario_id_filtro):
    """
    Crea un subgrafo que contiene solo los nodos que están asociados con un domiciliario específico,
    y las aristas que conectan esos nodos.

    Args:
        grafo_original (dict): El grafo principal de domicilios.
        domiciliario_id_filtro (str): El ID del domiciliario por el cual filtrar los nodos.

    Returns:
        dict: Un nuevo objeto grafo (mi_grafo) que es el subgrafo filtrado.
    """
    
    # Crear un nuevo grafo vacío para el subgrafo
    # Usar el orden del original como capacidad inicial para los mapas del subgrafo.
    subgrafo = g.new_graph(g.order(grafo_original), directed=False) 

    # Mapa auxiliar para rastrear los vértices del subgrafo ya añadidos
    nodos_en_subgrafo = map.new_map(g.order(grafo_original), 0.5)

    # 1. Identificar y añadir vértices al subgrafo que contengan al domiciliario
    claves_vertices_originales = g.vertices(grafo_original) # Obtener todas las claves de vértices del grafo original

    for i in range(lt.size(claves_vertices_originales)):
        clave_vertice = lt.get_element(claves_vertices_originales, i)
        
        # Obtener la lista de IDs de domiciliarios asociada a este vértice (es el 'value' del nodo)
        lista_domiciliarios_nodo = g.get_vertex_info(grafo_original, clave_vertice)
        
        domiciliario_encontrado_en_nodo = False
        if lista_domiciliarios_nodo is not None:
            # Iterar manualmente sobre la lista de domiciliarios para verificar la presencia
            idx_dom = 0
            while idx_dom < lt.size(lista_domiciliarios_nodo) and not domiciliario_encontrado_en_nodo:
                if lt.get_element(lista_domiciliarios_nodo, idx_dom) == domiciliario_id_filtro:
                    domiciliario_encontrado_en_nodo = True
                idx_dom += 1
        
        if domiciliario_encontrado_en_nodo:
            # Si el nodo contiene al domiciliario, añadirlo al subgrafo
            # El valor del nodo en el subgrafo será la misma lista de domiciliarios (copia por referencia, lo cual es OK)
            g.insert_vertex(subgrafo, clave_vertice, lista_domiciliarios_nodo)
            map.put(nodos_en_subgrafo, clave_vertice, True) # Marcar que este nodo está en el subgrafo

    # 2. Añadir aristas al subgrafo (solo si ambos extremos están en el subgrafo)
    # Iterar sobre todos los vértices que acabamos de añadir al subgrafo
    claves_vertices_subgrafo = map.key_set(nodos_en_subgrafo) # Obtener las claves de los nodos que están en el subgrafo

    for i in range(lt.size(claves_vertices_subgrafo)):
        clave_u = lt.get_element(claves_vertices_subgrafo, i)
        
        # Obtener los adyacentes de 'u' en el grafo ORIGINAL (para ver las aristas)
        # g.adjacents() devuelve un array_list de claves de vecinos
        adyacentes_u_original = g.adjacents(grafo_original, clave_u) 
        
        if adyacentes_u_original is not None:
            for j in range(lt.size(adyacentes_u_original)):
                clave_v = lt.get_element(adyacentes_u_original, j)
                
                # Verificar si el vecino 'v' también está en el subgrafo
                if map.get(nodos_en_subgrafo, clave_v) is not None:
                    # Si ambos 'u' y 'v' están en el subgrafo, añadir la arista entre ellos.
                    # El peso debe ser el original.
                    
                    # Obtener la arista completa desde el grafo original (mapa de adyacencia de u)
                    mapa_adyacencia_u_original = g.get_adjacents(grafo_original, clave_u) # Esto devuelve un mapa
                    arista_original = map.get(mapa_adyacencia_u_original, clave_v)
                    peso_arista = arista_original['weight']
                    
                    # Añadir la arista al subgrafo. g.add_edge se encarga de la no-direccionalidad
                    # y la no-paralelidad, y de contar el num_edges.
                    g.add_edge(subgrafo, clave_u, clave_v, peso_arista)

    return subgrafo
        
def req_7(catalog, punto_A_id, domiciliario_id):

    info_punto_A = g.get_vertex_info(catalog['grafo_domicilios'], punto_A_id)
    if info_punto_A is None:
        return {
            'cantidad_ubicaciones_subred': 0,
            'identificadores_subred_ordenados': lt.new_list(),
            'peso_total_mst': 0.0,
            'valido': False, 'mensaje_error': f"El punto de origen '{punto_A_id}' no existe en el grafo principal."
        }

    domiciliario_en_origen = False
    if info_punto_A is not None:
        idx_dom = 0
        while idx_dom < lt.size(info_punto_A) and not domiciliario_en_origen:
            if lt.get_element(info_punto_A, idx_dom) == domiciliario_id:
                domiciliario_en_origen = True
            idx_dom += 1
    
    if not domiciliario_en_origen:
        return {
            'cantidad_ubicaciones_subred': 0,
            'identificadores_subred_ordenados': lt.new_list(),
            'peso_total_mst': 0.0,
            'valido': False, 'mensaje_error': f"El punto de origen '{punto_A_id}' no está asociado con el domiciliario '{domiciliario_id}'. No se puede iniciar el MST."
        }

 
    grafo_filtrado = crear_subgrafo_para_domiciliario(catalog['grafo_domicilios'], domiciliario_id)

    if g.order(grafo_filtrado) == 0:
        return {
            'cantidad_ubicaciones_subred': 0,
            'identificadores_subred_ordenados': lt.new_list(),
            'peso_total_mst': 0.0,
            'valido': False, 'mensaje_error': f"No se encontraron ubicaciones para el domiciliario '{domiciliario_id}'. El subgrafo está vacío."
        }
    if g.get_vertex_info(grafo_filtrado, punto_A_id) is None:
        return {
            'cantidad_ubicaciones_subred': 0,
            'identificadores_subred_ordenados': lt.new_list(),
            'peso_total_mst': 0.0,
            'valido': False, 'mensaje_error': f"El punto de origen '{punto_A_id}' no existe en el subgrafo del domiciliario '{domiciliario_id}'."
        }
    
    #Ejecutar el algoritmo de Prim's en el SUBGRAFO filtrado
  
    prim_results = prim.prim_mst(grafo_filtrado, punto_A_id)

    # 4. Extraer y calcular los resultados
    
    cantidad_ubicaciones_subred = 0
    identificadores_subred_list_py = []
    
    marked_nodes_keys_lt = map.key_set(prim_results['marked']) 
    for i in range(lt.size(marked_nodes_keys_lt)):
        node_id = lt.get_element(marked_nodes_keys_lt, i)
        if map.get(prim_results['marked'], node_id) == True:
            cantidad_ubicaciones_subred += 1
            identificadores_subred_list_py.append(node_id)
    

    identificadores_subred_list_py.sort()

 
    identificadores_subred_ordenados_lt = lt.new_list()
    for id_val in identificadores_subred_list_py:
        lt.add_last(identificadores_subred_ordenados_lt, id_val)


    peso_total_mst = prim.weight_mst(grafo_filtrado, prim_results)
    
    # 6. Preparar el diccionario de respuesta
    result = {
        'cantidad_ubicaciones_subred': cantidad_ubicaciones_subred,
        'identificadores_subred_ordenados': identificadores_subred_ordenados_lt,
        'peso_total_mst': peso_total_mst,
        'valido': True,
        'origen_valido': True, # Se pudo iniciar desde el origen
        'mensaje_error': None
    }
    
    # Advertencia si el MST no conectó todos los nodos del subgrafo (si el subgrafo no es conexo)
    if cantidad_ubicaciones_subred < g.order(grafo_filtrado):
        result['mensaje_error'] = f"Advertencia: Prim's no conectó todas las {g.order(grafo_filtrado)} ubicaciones del subgrafo ({cantidad_ubicaciones_subred} conectadas). El subgrafo filtrado no es conexo desde el origen."
    
    return result
        
    
def req_8(catalog, centro_id, radio_km, dp_id):

    lat_str, lon_str = centro_id.split('_')
    lat_c, lon_c = float(lat_str), float(lon_str)
    mapa = folium.Map(location=[lat_c, lon_c], zoom_start=13)
    folium.Circle(
        location=[lat_c, lon_c],
        radius=radio_km * 1000,
        color='blue', weight=3, fill=False, opacity=0.5
    ).add_to(mapa)

    def _haversine(a_lat, a_lon, b_lat, b_lon):
        R = 6371.0
        φ1 = math.radians(a_lat)
        φ2 = math.radians(b_lat)
        dφ = math.radians(b_lat - a_lat)
        dλ = math.radians(b_lon - a_lon)
        a = math.sin(dφ/2)**2 + math.cos(φ1)*math.cos(φ2)*math.sin(dλ/2)**2
        return 2 * R * math.asin(math.sqrt(a))

    todos = g.vertices(catalog['grafo_domicilios'])
    region = lt.new_list()                       # lista de vid en región
    coords = map.new_map(lt.size(todos), 0.5)    # vid -> (lat, lon)

    for i in range(lt.size(todos)):
        vid = lt.get_element(todos, i)
        info_list = g.get_vertex_info(catalog['grafo_domicilios'], vid) or []

        # comprobar pertenencia usando lt
        pertenece = False
        for j in range(lt.size(info_list)):
            if lt.get_element(info_list, j) == dp_id:
                pertenece = True
                break
        if not pertenece:
            continue

        # parsear coords del vid
        lat_s, lon_s = vid.split('_')
        lat_v, lon_v = float(lat_s), float(lon_s)

        # filtrar por distancia
        if _haversine(lat_c, lon_c, lat_v, lon_v) <= radio_km:
            lt.add_last(region, vid)
            map.put(coords, vid, (lat_v, lon_v))

    if lt.size(region) == 0:
        return None

    for k in range(lt.size(region)):
        vid = lt.get_element(region, k)
        lat_v, lon_v = map.get(coords, vid)
        folium.CircleMarker(
            location=[lat_v, lon_v],
            radius=5,
            color='green',
            fill=True,
            fill_color='green',
            popup=vid
        ).add_to(mapa)

    if lt.size(region) > 1:
        path = []
        for k in range(lt.size(region)):
            vid = lt.get_element(region, k)
            path.append(map.get(coords, vid))
        folium.PolyLine(locations=path, color='red', weight=3, opacity=0.8).add_to(mapa)

    base = os.path.dirname(__file__)
    out_dir = os.path.abspath(os.path.join(base, '..', 'Data'))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'recorrido_domiciliario.html')
    mapa.save(out_path)

    return out_path  
    


        
        
        
        
        
