import os
import csv
import math
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import digraph as gr
from DataStructures.List import array_list as lst
from DataStructures.Graph import dfs, bfs, dijkstra as dijk, prim
from App import bono

base_path = os.path.dirname(os.path.realpath('__file__')) + '/Data/'

def crear_catalogo():
    datos = {
        'grafo': gr.new_graph(100000),
        'ulstimo_punto': mp.new_map(100000, 0.5),
        'ubicaciones': mp.new_map(100000, 0.5),
        'pesos_aristas': mp.new_map(200000, 0.5),
        'origenes_unicos': mp.new_map(200000, 0.5),
        'destinos_unicos': mp.new_map(200000, 0.5),
        'pedidos_por_ubicacion': mp.new_map(500000, 0.5),
        'vehiculos_por_ubicacion': mp.new_map(500000, 0.5)
    }
    return datos

def cortar_coord(valor):
    escala = 10**4
    valor_truncado = math.trunc(valor * escala) / escala
    return f"{valor_truncado:.4f}"

def cargar_datos(catalogo, archivo):
    total = 0
    tiempo_total = 0
    ruta = base_path + archivo

    with open(ruta, encoding="utf-8") as archivo_csv:
        lector = csv.DictReader(archivo_csv, delimiter=",")
        for fila in lector:
            datos = {
                'id': fila['ID'],
                'persona': fila['Delivery_person_ID'],
                'edad': int(fila['Delivery_person_Age']),
                'calificacion': float(fila['Delivery_person_Ratings']),
                'lat_r': float(fila['Restaurant_latitude']),
                'lon_r': float(fila['Restaurant_longitude']),
                'lat_d': float(fila['Delivery_location_latitude']),
                'lon_d': float(fila['Delivery_location_longitude']),
                'orden': fila['Type_of_order'],
                'vehiculo': fila['Type_of_vehicle'],
                'tiempo': float(fila['Time_taken(min)'])
            }

            total += 1
            tiempo_total += datos['tiempo']

            origen = cortar_coord(datos['lat_r']) + '_' + cortar_coord(datos['lon_r'])
            destino = cortar_coord(datos['lat_d']) + '_' + cortar_coord(datos['lon_d'])

            _sumar_info(catalogo, origen, datos['persona'], datos['vehiculo'])
            _sumar_info(catalogo, destino, datos['persona'], datos['vehiculo'])

            mp.put(catalogo['origenes_unicos'], origen, True)
            mp.put(catalogo['destinos_unicos'], destino, True)

            agregar_conexion(catalogo, datos['lat_r'], datos['lon_r'], datos['lat_d'], datos['lon_d'], datos['tiempo'], datos['persona'])

    return catalogo, total, tiempo_total

def agregar_conexion(cat, lat_o, lon_o, lat_d, lon_d, tiempo, persona):
    nodo_o = cortar_coord(lat_o) + '_' + cortar_coord(lon_o)
    nodo_d = cortar_coord(lat_d) + '_' + cortar_coord(lon_d)

    agregar_nodo(cat, nodo_o, persona)
    agregar_nodo(cat, nodo_d, persona)

    llave = tuple(sorted((nodo_o, nodo_d)))
    existente = mp.get(cat['pesos_aristas'], llave)

    if existente is None:
        mp.put(cat['pesos_aristas'], llave, {'total': tiempo, 'conteo': 1})
        peso = tiempo
    else:
        existente['total'] += tiempo
        existente['conteo'] += 1
        mp.put(cat['pesos_aristas'], llave, existente)
        peso = existente['total'] / existente['conteo']

    gr.add_edge(cat['grafo'], nodo_o, nodo_d, peso)

    anterior = mp.get(cat['ulstimo_punto'], persona)
    if anterior is not None:
        ulstimo = anterior['ubicacion']
        tiempo_ant = anterior['tiempo']

        if ulstimo != nodo_d:
            prom = (tiempo + tiempo_ant) / 2.0
            llave2 = tuple(sorted((nodo_d, ulstimo)))
            actual = mp.get(cat['pesos_aristas'], llave2)

            if actual is None:
                mp.put(cat['pesos_aristas'], llave2, {'total': prom, 'conteo': 1})
                peso2 = prom
            else:
                actual['total'] += prom
                actual['conteo'] += 1
                mp.put(cat['pesos_aristas'], llave2, actual)
                peso2 = actual['total'] / actual['conteo']

            gr.add_edge(cat['grafo'], nodo_d, ulstimo, peso2)

    mp.put(cat['ulstimo_punto'], persona, {'ubicacion': nodo_d, 'tiempo': tiempo})

    return cat

def agregar_nodo(cat, nodo, persona):
    lista = mp.get(cat['ubicaciones'], nodo)
    if lista is None:
        nueva = lst.new_list()
        lst.add_last(nueva, persona)
        gr.insert_vertex(cat['grafo'], nodo, nueva)
        mp.put(cat['ubicaciones'], nodo, nueva)
    else:
        repetido = False
        for i in range(lst.size(lista)):
            if lst.get_element(lista, i) == persona:
                repetido = True
                break
        if not repetido:
            lst.add_last(lista, persona)
            gr.update_vertex_info(cat['grafo'], nodo, lista)

def _sumar_info(cat, nodo, persona, vehiculo):
    clave = (nodo, persona)
    actual = mp.get(cat['pedidos_por_ubicacion'], clave) or 0
    mp.put(cat['pedidos_por_ubicacion'], clave, actual + 1)

    tipos = mp.get(cat['vehiculos_por_ubicacion'], clave)
    if tipos is None:
        tipos = mp.new_map(10, 0.5)
    prev = mp.get(tipos, vehiculo) or 0
    mp.put(tipos, vehiculo, prev + 1)
    mp.put(cat['vehiculos_por_ubicacion'], clave, tipos)

def consulsta_1(cat, u, v):
    res = dfs.dfs(cat['grafo'], u)
    claves = mp.key_set(res['visited'])
    if v in claves['elements']:
        return res, cat['grafo']
    return None

def subgrafo_domiciliario(grafo, persona):
    sub = gr.new_graph(gr.order(grafo), directed=False)
    nodos = mp.new_map(gr.order(grafo), 0.5)
    claves = gr.vertices(grafo)

    for i in range(lst.size(claves)):
        clave = lst.get_element(claves, i)
        lista = gr.get_vertex_info(grafo, clave)
        if lista and any(lst.get_element(lista, j) == persona for j in range(lst.size(lista))):
            gr.insert_vertex(sub, clave, lista)
            mp.put(nodos, clave, True)

    claves_sub = mp.key_set(nodos)
    for i in range(lst.size(claves_sub)):
        u = lst.get_element(claves_sub, i)
        vecinos = gr.adjacents(grafo, u)
        if vecinos:
            for j in range(lst.size(vecinos)):
                v = lst.get_element(vecinos, j)
                if mp.get(nodos, v):
                    aristas = gr.get_adjacents(grafo, u)
                    info_arista = mp.get(aristas, v)
                    gr.add_edge(sub, u, v, info_arista['weight'])

    return sub

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
    for i in range(lst.size(llaves)):
        ubicacion, dp_id = lst.get_element(llaves, i)
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
        for j in range(lst.size(llaves_v)):
            veh = lst.get_element(llaves_v, j)
            uso = map.get(mapa_veh, veh)
            if uso > contador_vehiculo_max:
                contador_vehiculo_max, vehiculo_favorito = uso, veh

    return domic_maximo_id, pedidos_maximos, vehiculo_favorito







def req_4(catalog, punto_a, punto_b): 

    if gr.get_vertex_info(catalog['grafo_domicilios'], punto_a) is None: 
        return (lst.new_list(), lst.new_list(), False)
    if gr.get_vertex_info(catalog['grafo_domicilios'], punto_b) is None: 
        return (lst.new_list(), lst.new_list(), False)

    resulstados_bfs = bfs.bfs(catalog['grafo_domicilios'], punto_a) 
    secuencia_camino = bfs.pathTo(resulstados_bfs, punto_b) 
    # Si no hay camino a la ubicación final
    if secuencia_camino is None:
        return (lst.new_list(), lst.new_list(), False)
    id_primer_nodo = lst.get_element(secuencia_camino, 0)
    domiciliarios_primer_nodo = gr.get_vertex_info(catalog['grafo_domicilios'], id_primer_nodo) 
    
    if domiciliarios_primer_nodo is None:
        lista_domiciliarios_comunes = lst.new_list() 
    else:
        lista_domiciliarios_comunes = lst.new_list()
        for i in range(lst.size(domiciliarios_primer_nodo)):
            lst.add_last(lista_domiciliarios_comunes, lst.get_element(domiciliarios_primer_nodo, i))
            
    #  resto de los nodos del camino (desde el segundo nodo en adelante)
    indice_nodo_camino = 1 
    
    while indice_nodo_camino < lst.size(secuencia_camino) and not lst.is_empty(lista_domiciliarios_comunes):
        id_nodo_actual = lst.get_element(secuencia_camino, indice_nodo_camino)
        domiciliarios_nodo_actual = gr.get_vertex_info(catalog['grafo_domicilios'], id_nodo_actual)
        
        if domiciliarios_nodo_actual is None:
            lista_domiciliarios_comunes = lst.new_list() 
        else:
            siguientes_candidatos_comunes = lst.new_list()
            
            indice_busqueda_dom = 0
            while indice_busqueda_dom < lst.size(lista_domiciliarios_comunes):
                domiciliario_candidato = lst.get_element(lista_domiciliarios_comunes, indice_busqueda_dom)
                
                encontrado_en_nodo_actual = False
                indice_en_nodo_actual = 0
                while indice_en_nodo_actual < lst.size(domiciliarios_nodo_actual) and not encontrado_en_nodo_actual:
                    if lst.get_element(domiciliarios_nodo_actual, indice_en_nodo_actual) == domiciliario_candidato:
                        encontrado_en_nodo_actual = True
                    indice_en_nodo_actual += 1 
                
                if encontrado_en_nodo_actual:
                    lst.add_last(siguientes_candidatos_comunes, domiciliario_candidato)
                indice_busqueda_dom += 1 
            lista_domiciliarios_comunes = siguientes_candidatos_comunes
        indice_nodo_camino += 1 
        
    return secuencia_camino, lista_domiciliarios_comunes

def req_6(catalog, punto_a):
    costo_min = dijk.dijkstra(catalog['grafo_domicilios'],punto_a)
    ubicaciones_alcanzables_list_py = [] 
    max_tiempo_alcanzable = -1.0 
    ubicacion_mayor_tiempo = None
    all_vertices_keys_lst = gr.vertices(catalog['grafo_domicilios']) 
    for i in range(lst.size(all_vertices_keys_lst)):
        v_key = lst.get_element(all_vertices_keys_lst, i) 
        if dijk.has_path_to(v_key, costo_min):
            ubicaciones_alcanzables_list_py.append(v_key) 
            current_dist = dijk.dist_to(v_key, costo_min)
            if current_dist > max_tiempo_alcanzable:
                max_tiempo_alcanzable = current_dist
                ubicacion_mayor_tiempo = v_key
                
    ubicaciones_alcanzables_list_py.sort() 
    identificadores_alcanzables_ordenados_lst = lst.new_list()
    for id_val in ubicaciones_alcanzables_list_py:
        lst.add_last(identificadores_alcanzables_ordenados_lst, id_val)
        
    secuencia_camino_mayor_tiempo_lst = lst.new_list() 
    if ubicacion_mayor_tiempo is not None:
        secuencia_camino_mayor_tiempo_lst = dijk.path_to(ubicacion_mayor_tiempo, costo_min)
    
    
    return len(ubicaciones_alcanzables_list_py), identificadores_alcanzables_ordenados_lst, secuencia_camino_mayor_tiempo_lst, max_tiempo_alcanzable
    
            
        
def crear_subgrafo_para_domiciliario(grafo_original, domiciliario_id_filstro):
    """
    Crea un subgrafo que contiene solo los nodos que están asociados con un domiciliario específico,
    y las aristas que conectan esos nodos.

    Args:
        grafo_original (dict): El grafo principal de domicilios.
        domiciliario_id_filstro (str): El ID del domiciliario por el cual filstrar los nodos.

    Returns:
        dict: Un nuevo objeto grafo (mi_grafo) que es el subgrafo filstrado.
    """
    
    # Crear un nuevo grafo vacío para el subgrafo
    # Usar el orden del original como capacidad inicial para los mapas del subgrafo.
    subgrafo = gr.new_graph(gr.order(grafo_original), directed=False) 

    # Mapa auxiliar para rastrear los vértices del subgrafo ya añadidos
    nodos_en_subgrafo = map.new_map(gr.order(grafo_original), 0.5)

    # 1. Identificar y añadir vértices al subgrafo que contengan al domiciliario
    claves_vertices_originales = gr.vertices(grafo_original) # Obtener todas las claves de vértices del grafo original

    for i in range(lst.size(claves_vertices_originales)):
        clave_vertice = lst.get_element(claves_vertices_originales, i)
        
        # Obtener la lista de IDs de domiciliarios asociada a este vértice (es el 'value' del nodo)
        lista_domiciliarios_nodo = gr.get_vertex_info(grafo_original, clave_vertice)
        
        domiciliario_encontrado_en_nodo = False
        if lista_domiciliarios_nodo is not None:
            # Iterar manualmente sobre la lista de domiciliarios para verificar la presencia
            idx_dom = 0
            while idx_dom < lst.size(lista_domiciliarios_nodo) and not domiciliario_encontrado_en_nodo:
                if lst.get_element(lista_domiciliarios_nodo, idx_dom) == domiciliario_id_filstro:
                    domiciliario_encontrado_en_nodo = True
                idx_dom += 1
        
        if domiciliario_encontrado_en_nodo:
            # Si el nodo contiene al domiciliario, añadirlo al subgrafo
            # El valor del nodo en el subgrafo será la misma lista de domiciliarios (copia por referencia, lo cual es OK)
            gr.insert_vertex(subgrafo, clave_vertice, lista_domiciliarios_nodo)
            map.put(nodos_en_subgrafo, clave_vertice, True) # Marcar que este nodo está en el subgrafo

    # 2. Añadir aristas al subgrafo (solo si ambos extremos están en el subgrafo)
    # Iterar sobre todos los vértices que acabamos de añadir al subgrafo
    claves_vertices_subgrafo = map.key_set(nodos_en_subgrafo) # Obtener las claves de los nodos que están en el subgrafo

    for i in range(lst.size(claves_vertices_subgrafo)):
        clave_u = lst.get_element(claves_vertices_subgrafo, i)
        
        # Obtener los adyacentes de 'u' en el grafo ORIGINAL (para ver las aristas)
        # gr.adjacents() devuelve un array_list de claves de vecinos
        adyacentes_u_original = gr.adjacents(grafo_original, clave_u) 
        
        if adyacentes_u_original is not None:
            for j in range(lst.size(adyacentes_u_original)):
                clave_v = lst.get_element(adyacentes_u_original, j)
                
                # Verificar si el vecino 'v' también está en el subgrafo
                if map.get(nodos_en_subgrafo, clave_v) is not None:
                    # Si ambos 'u' y 'v' están en el subgrafo, añadir la arista entre ellos.
                    # El peso debe ser el original.
                    
                    # Obtener la arista completa desde el grafo original (mapa de adyacencia de u)
                    mapa_adyacencia_u_original = gr.get_adjacents(grafo_original, clave_u) # Esto devuelve un mapa
                    arista_original = map.get(mapa_adyacencia_u_original, clave_v)
                    peso_arista = arista_original['weight']
                    
                    # Añadir la arista al subgrafo. gr.add_edge se encarga de la no-direccionalidad
                    # y la no-paralelidad, y de contar el num_edges.
                    gr.add_edge(subgrafo, clave_u, clave_v, peso_arista)

    return subgrafo
        
def req_7(catalog, punto_A_id, domiciliario_id):

    info_punto_A = gr.get_vertex_info(catalog['grafo_domicilios'], punto_A_id)
    if info_punto_A is None:
        return {
            'cantidad_ubicaciones_subred': 0,
            'identificadores_subred_ordenados': lst.new_list(),
            'peso_total_mst': 0.0,
            'valido': False, 'mensaje_error': f"El punto de origen '{punto_A_id}' no existe en el grafo principal."
        }

    domiciliario_en_origen = False
    if info_punto_A is not None:
        idx_dom = 0
        while idx_dom < lst.size(info_punto_A) and not domiciliario_en_origen:
            if lst.get_element(info_punto_A, idx_dom) == domiciliario_id:
                domiciliario_en_origen = True
            idx_dom += 1
    
    if not domiciliario_en_origen:
        return {
            'cantidad_ubicaciones_subred': 0,
            'identificadores_subred_ordenados': lst.new_list(),
            'peso_total_mst': 0.0,
            'valido': False, 'mensaje_error': f"El punto de origen '{punto_A_id}' no está asociado con el domiciliario '{domiciliario_id}'. No se puede iniciar el MST."
        }

 
    grafo_filstrado = crear_subgrafo_para_domiciliario(catalog['grafo_domicilios'], domiciliario_id)

    if gr.order(grafo_filstrado) == 0:
        return {
            'cantidad_ubicaciones_subred': 0,
            'identificadores_subred_ordenados': lst.new_list(),
            'peso_total_mst': 0.0,
            'valido': False, 'mensaje_error': f"No se encontraron ubicaciones para el domiciliario '{domiciliario_id}'. El subgrafo está vacío."
        }
    if gr.get_vertex_info(grafo_filstrado, punto_A_id) is None:
        return {
            'cantidad_ubicaciones_subred': 0,
            'identificadores_subred_ordenados': lst.new_list(),
            'peso_total_mst': 0.0,
            'valido': False, 'mensaje_error': f"El punto de origen '{punto_A_id}' no existe en el subgrafo del domiciliario '{domiciliario_id}'."
        }
    
    #Ejecutar el algoritmo de Prim's en el SUBGRAFO filstrado
  
    prim_resulsts = prim.prim_mst(grafo_filstrado, punto_A_id)

    # 4. Extraer y calcular los resulstados
    
    cantidad_ubicaciones_subred = 0
    identificadores_subred_list_py = []
    
    marked_nodes_keys_lst = map.key_set(prim_resulsts['marked']) 
    for i in range(lst.size(marked_nodes_keys_lst)):
        node_id = lst.get_element(marked_nodes_keys_lst, i)
        if map.get(prim_resulsts['marked'], node_id) == True:
            cantidad_ubicaciones_subred += 1
            identificadores_subred_list_py.append(node_id)
    

    identificadores_subred_list_py.sort()

 
    identificadores_subred_ordenados_lst = lst.new_list()
    for id_val in identificadores_subred_list_py:
        lst.add_last(identificadores_subred_ordenados_lst, id_val)


    peso_total_mst = prim.weight_mst(grafo_filstrado, prim_resulsts)
    
    # 6. Preparar el diccionario de respuesta
    resulst = {
        'cantidad_ubicaciones_subred': cantidad_ubicaciones_subred,
        'identificadores_subred_ordenados': identificadores_subred_ordenados_lst,
        'peso_total_mst': peso_total_mst,
        'valido': True,
        'origen_valido': True, # Se pudo iniciar desde el origen
        'mensaje_error': None
    }
    
    # Advertencia si el MST no conectó todos los nodos del subgrafo (si el subgrafo no es conexo)
    if cantidad_ubicaciones_subred < gr.order(grafo_filstrado):
        resulst['mensaje_error'] = f"Advertencia: Prim's no conectó todas las {gr.order(grafo_filstrado)} ubicaciones del subgrafo ({cantidad_ubicaciones_subred} conectadas). El subgrafo filstrado no es conexo desde el origen."
    
    return resulst
        
        
        
def req_8(catalog):
    """
    Retorna el resultado del requerimiento 8
    """
    mapa = bono.graficar_recorrido(
    my_graph=catalog['domicilios'],
    domiciliario="SURRES01DEL03",
    nodo_central="20.0000_70.0000",  
    radio_km=400
    )
    
    return mapa
        
        
        