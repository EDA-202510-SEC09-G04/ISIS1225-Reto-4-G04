
from DataStructures.Graph import digraph as gr  # Asumiendo que usas tu estructura de grafo
from math import radians, sin, cos, sqrt, atan2
import folium


def generar_mapa(my_graph, archivo_salida="mapa_domicilios.html"):
    # 1. Crear mapa centrado en Bogotá (ejemplo)
    mapa = folium.Map(location=[4.6097, -74.0817], zoom_start=12)

    # 2. Diccionarios para almacenar ubicaciones únicas
    restaurantes = {}
    destinos = {}

    # 3. Recorrer todos los vértices del grafo
    for node_id in gr.vertices(my_graph)['elements']:
        node_info = gr.get_vertex_information(my_graph, node_id)
        lat, lon = map(float, node_id.split("_"))  # Formato: "lat_lon"
        
        if node_info['info']['tipo'] == 'restaurante':
            restaurantes[node_id] = (lat, lon)
        else:
            destinos[node_id] = (lat, lon)

    # 4. Agregar marcadores al mapa
    # Restaurantes (rojo)
    for node_id, (lat, lon) in restaurantes.items():
        folium.Marker(
            location=[lat, lon],
            popup=f"Restaurante: {node_id}",
            icon=folium.Icon(color="red", icon="cutlery")
        ).add_to(mapa)

    # Destinos (azul)
    for node_id, (lat, lon) in destinos.items():
        folium.Marker(
            location=[lat, lon],
            popup=f"Destino: {node_id}",
            icon=folium.Icon(color="blue", icon="home")
        ).add_to(mapa)

    # 5. Opcional: Conectar restaurantes con destinos (líneas verdes)
    for node_id in restaurantes:
        adjacents = gr.adjacents(my_graph, node_id)
        for neighbor in adjacents['elements']:
            if neighbor in destinos:
                folium.PolyLine(
                    locations=[
                        [float(x) for x in node_id.split("_")],
                        [float(x) for x in neighbor.split("_")]
                    ],
                    color="green",
                    weight=2
                ).add_to(mapa)

    # 6. Guardar mapa como HTML
    mapa.save(archivo_salida)
    print(f"Mapa generado: {archivo_salida}")




def distancia_haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia en km entre dos puntos geográficos.
    """
    R = 6371  # Radio de la Tierra en km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c
""" 

def filtrar_pedidos_en_radio(historial, domiciliario, centro, radio):
    if domiciliario not in historial:
        return []
    
    lat_central, lon_central = map(float, centro.split("_"))
    
    pedidos_en_radio = []
    for rest, dest in historial[domiciliario]:
        lat, lon = map(float, dest.split("_"))
        distancia = distancia_haversine(lat_central, lon_central, lat, lon)
        if distancia <= radio:
            pedidos_en_radio.append((rest, dest))
    
    return pedidos_en_radio

 """
def filtrar_pedidos_en_radio(historial, domiciliario, nodo_central, radio_km, my_graph):
    """
    Retorna los pedidos del domiciliario que están dentro del radio.
    Imprime información de debug para verificar nodos y adyacencias.
    """
    
    if domiciliario not in historial:
        print(f"❌ El domiciliario '{domiciliario}' no existe en el historial.")
        return []
    
    # Obtener coordenadas del nodo central
    lat_central, lon_central = map(float, nodo_central.split("_"))
    
    pedidos_en_radio = []
    print(f"\n🔍 Debug: Filtrado para domiciliario '{domiciliario}' en radio {radio_km} km desde nodo {nodo_central}")
    
    for i, (rest, dest) in enumerate(historial[domiciliario]):
        # Calcular distancia para el DESTINO
        lat_dest, lon_dest = map(float, dest.split("_"))
        distancia = distancia_haversine(lat_central, lon_central, lat_dest, lon_dest)
        
        if distancia <= radio_km:
            print(f"\n✅ Pedido {i+1} DENTRO del radio ({distancia:.2f} km):")
            print(f"   - Restaurante: {rest}")
            print(f"   - Destino: {dest}")
            
            # Debug: Información de adyacencias del DESTINO
            print("\n   🔗 Adyacencias del Destino:")
            adjacents = gr.adjacents(my_graph, dest)['elements']
            for vecino in adjacents:
                peso = gr.get_edge(my_graph, dest, vecino)
                print(f"      → {vecino} (Peso: {peso:.1f} min)")
            
            pedidos_en_radio.append((rest, dest))
        else:
            print(f"❌ Pedido {i+1} FUERA del radio ({distancia:.2f} km): Destino {dest}")
    
    print(f"\n📌 Total pedidos válidos: {len(pedidos_en_radio)}")
    return pedidos_en_radio

def graficar_recorrido(my_graph, domiciliario, nodo_central, radio_km):
    
    historial = my_graph['historial']
    # 1. Filtrar pedidos en el radio (con debug)
    pedidos = filtrar_pedidos_en_radio(historial, domiciliario, nodo_central, radio_km, my_graph)
    
    if not pedidos:
        return
    
    # 2. Crear mapa centrado en el nodo central
    lat_central, lon_central = map(float, nodo_central.split("_"))
    mapa = folium.Map(location=[lat_central, lon_central], zoom_start=12)
    
    # 3. Dibujar radio de búsqueda
    folium.Circle(
        location=[lat_central, lon_central],
        radius=radio_km * 1000,
        color="#3186cc",
        fill=True,
        fill_opacity=0.2
    ).add_to(mapa)
    
    # 4. Procesar cada pedido válido
    restaurantes_plot = set()
    destinos_plot = set()
    
    for i, (rest, dest) in enumerate(pedidos):
        # Coordenadas
        lat_rest, lon_rest = map(float, rest.split("_"))
        lat_dest, lon_dest = map(float, dest.split("_"))
        
        # Agregar RESTAURANTE (si no está ya)
        if rest not in restaurantes_plot:
            folium.Marker(
                location=[lat_rest, lon_rest],
                popup=f"Restaurante (Pedido {i+1})",
                icon=folium.Icon(color="green", icon="cutlery")
            ).add_to(mapa)
            restaurantes_plot.add(rest)
        
        # Agregar DESTINO (si no está ya)
        if dest not in destinos_plot:
            folium.Marker(
                location=[lat_dest, lon_dest],
                popup=f"Destino (Pedido {i+1})",
                icon=folium.Icon(color="red", icon="home")
            ).add_to(mapa)
            destinos_plot.add(dest)
        
        # Dibujar conexión RESTAURANTE → DESTINO (si no existe)
        folium.PolyLine(
            locations=[[lat_rest, lon_rest], [lat_dest, lon_dest]],
            color="blue",
            weight=2.5,
            popup=f"Pedido {i+1} (Peso: {gr.get_edge(my_graph, rest, dest):.1f} min)"
        ).add_to(mapa)
    
    # 5. Dibujar adyacencias VÁLIDAS entre destinos (excluyendo peso 0)
    for dest in destinos_plot:
        for vecino in gr.adjacents(my_graph, dest)['elements']:
            peso = gr.get_edge(my_graph, dest, vecino)
            if vecino in destinos_plot and peso > 0:  # Solo conexiones válidas
                lat1, lon1 = map(float, dest.split("_"))
                lat2, lon2 = map(float, vecino.split("_"))
                folium.PolyLine(
                    locations=[[lat1, lon1], [lat2, lon2]],
                    color="orange",
                    weight=1.5,
                    dash_array="5,5",
                    popup=f"Conexión D-D (Peso: {peso:.1f} min)"
                ).add_to(mapa)
    
    mapa.save('archivo_salida.html')
    print(f"Mapa generado")