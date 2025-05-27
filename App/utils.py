from DataStructures.Utils import error as error
from DataStructures.Graph import digraph as gr
from DataStructures.Map import map_linear_probing as mp


def format_coord(coord):
    """
    Formatea una coordenada a exactamente 4 decimales TRUNCADOS (sin redondeo)
    Ejemplo: 12.345678 -> "12.3456" (no "12.3457")
    """
    try:
        # Convertir a string y separar parte entera y decimal
        str_coord = str(float(coord))
        if '.' in str_coord:
            integer_part, decimal_part = str_coord.split('.')
            # Tomar solo primeros 4 decimales (sin redondear)
            truncated_decimal = (decimal_part + '0000')[:4]
            return f"{integer_part}.{truncated_decimal}"
        else:
            return f"{str_coord}.0000"
    except ValueError:
        raise ValueError(f"Coordenada inválida: {coord}")

def format_location(lat, lon):
    """Combina coordenadas formateadas con truncamiento"""
    return f"{format_coord(lat)}_{format_coord(lon)}"


def calcular_peso(my_graph, origen, destino):
    nodo_origen = gr.get_vertex_information(my_graph, origen) or {}
    tiempos = nodo_origen.get('info', {}).get('tiempos', {}).get(destino, [])
    return sum(tiempos)/len(tiempos) if tiempos else 0

def contar_tipos_nodos(my_graph):
    vertices = gr.vertices(my_graph)
            
    num_restaurantes = 0
    num_destinos = 0

    for node_id in vertices['elements']:
        node_info = gr.get_vertex_information(my_graph, node_id)
    
        tipo = node_info['info']['tipo']

        if tipo == 'restaurante':
            num_restaurantes += 1
        elif tipo == 'destino':
            num_destinos += 1
    return num_restaurantes, num_destinos
    
    

def crear_nodo(my_graph, node_id, connected_to, repartidor, tiempo, tipo):
    """Versión corregida sin duplicación de estructura"""
    tiempo_int = int(tiempo)
    
    # Obtener nodo existente o crear uno nuevo
    if not gr.contains_vertex(my_graph, node_id):
        
        info = {
                'tipo': tipo,
                'domiciliarios': [repartidor],
                'tiempos': {connected_to: [tiempo_int]}
        }
        
        return gr.insert_vertex(my_graph, node_id, info)
        
        
    else:
        # Obtener nodo existente (sin nivel extra)
        node = gr.get_vertex_information(my_graph, node_id)
        
        # Actualizar datos
        if repartidor not in node['info']['domiciliarios']:
            node['info']['domiciliarios'].append(repartidor)
            
        node['info']['tiempos'].setdefault(connected_to, []).append(tiempo_int)
        
        return gr.update_vertex_info(my_graph, node_id, node)
 
 
    
def print_node_info(graph, node_id):
    node = gr.get_vertex_information(graph, node_id) or {}
    info = node.get('info', {})
    print(f"\nNodo {node_id}:")
    print(f"Tipo: {info.get('tipo')}")
    print(f"Domiciliarios: {info.get('domiciliarios', [])}")
    print(f"Tiempos: {info.get('tiempos', {})}")
    
    

def actualizar_arista(my_graph, origen, destino, peso=None):
    """Versión con validación mejorada"""
    # Calcular peso si no se proporciona
    if peso is None:
        peso = calcular_peso(my_graph, origen, destino)
    
    # Validar nodos
    if not gr.contains_vertex(my_graph, origen) or not gr.contains_vertex(my_graph, destino):
        raise ValueError("Uno o ambos vértices no existen")
    
    origen_entry = mp.get(my_graph['vertices'], origen)
    destino_entry = mp.get(my_graph['vertices'], destino)
    
    # Inicializar adjacents si no existen
    origen_entry.setdefault('adjacents', mp.new_map(5, 0.5))
    destino_entry.setdefault('adjacents', mp.new_map(5, 0.5))
    
    # Verificar si es nueva arista
    es_nueva = not mp.contains(origen_entry['adjacents'], destino)
    
    # Actualizar ambas direcciones (grafo no dirigido)
    for u, v in [(origen, destino), (destino, origen)]:
        entry = mp.get(my_graph['vertices'], u)
        entry['adjacents'] = mp.put(entry['adjacents'], v, {'weight': peso})
        my_graph['vertices'] = mp.put(my_graph['vertices'], u, entry)
    
    # Actualizar contador
    if es_nueva:
        my_graph['num_edges'] += 1
    
    return my_graph

def debug_arista(graph, origen, destino):
    """Muestra información detallada de una arista"""
    print(f"\nDebugging arista {origen} ↔ {destino}:")
    
    # Verificar existencia de nodos
    if not gr.contains_vertex(graph, origen):
        print(f"¡El nodo {origen} no existe!")
        return
    if not gr.contains_vertex(graph, destino):
        print(f"¡El nodo {destino} no existe!")
        return
    
    # Obtener información
    origen_entry = mp.get(graph['vertices'], origen)
    destino_entry = mp.get(graph['vertices'], destino)
    
    print(f"Peso calculado: {calcular_peso(graph, origen, destino)}")
    
    # Verificar arista origen→destino
    if mp.contains(origen_entry['adjacents'], destino):
        peso = mp.get(origen_entry['adjacents'], destino)['weight']
        print(f"Arista {origen}→{destino}: EXISTE (peso: {peso})")
    else:
        print(f"Arista {origen}→{destino}: NO EXISTE")
    
    # Verificar arista destino→origen
    if mp.contains(destino_entry['adjacents'], origen):
        peso = mp.get(destino_entry['adjacents'], origen)['weight']
        print(f"Arista {destino}→{origen}: EXISTE (peso: {peso})")
    else:
        print(f"Arista {destino}→{origen}: NO EXISTE")

        

def procesar_historial(my_graph, historial, domiciliario, nuevo_pedido):
    """
    Versión actualizada que funciona con la nueva actualizar_arista()
    """
    if domiciliario not in historial:
        historial[domiciliario] = [nuevo_pedido]
        return my_graph
    
    if nuevo_pedido not in historial[domiciliario]:
        historial[domiciliario].append(nuevo_pedido)
    
    if len(historial[domiciliario]) < 2:
        return my_graph
    
    anterior, actual = historial[domiciliario][-2], historial[domiciliario][-1]
    destino_anterior = anterior[1]
    destino_actual = actual[1]
    
    peso_anterior = calcular_peso(my_graph, anterior[0], anterior[1])
    peso_actual = calcular_peso(my_graph, actual[0], actual[1])
    nuevo_peso = (peso_anterior + peso_actual) / 2
    
    # Ahora pasamos explícitamente el peso calculado
    return actualizar_arista(my_graph, destino_anterior, destino_actual, nuevo_peso)



def debug_historial(historial, domiciliario):
    """Muestra el estado del historial"""
    print(f"\nHistorial de {domiciliario}:")
    if domiciliario not in historial:
        print("  Sin historial registrado")
        return
    
    for i, (rest, dest) in enumerate(historial[domiciliario]):
        print(f"  {i+1}. Rest: {rest} → Dest: {dest}")
    
    if len(historial[domiciliario]) >= 2:
        print("\nÚltimas conexiones entre destinos:")
        for i in range(1, len(historial[domiciliario])):
            prev_dest = historial[domiciliario][i-1][1]
            curr_dest = historial[domiciliario][i][1]
            print(f"  {prev_dest} ↔ {curr_dest}")
