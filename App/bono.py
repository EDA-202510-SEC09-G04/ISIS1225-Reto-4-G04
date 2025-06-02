
from DataStructures.Graph import digraph as gr  # Asumiendo que usas tu estructura de grafo
from math import radians, sin, cos, sqrt, atan2
import folium
from DataStructures.List import array_list as lt
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
    
def req_8(catalog, centro_id, radio_km, dp_id):

    # 1) Parsear centro
    lat_str, lon_str = centro_id.split('_')
    lat_c, lon_c = float(lat_str), float(lon_str)

    # 2) Crear mapa y círculo
    mapa = folium.Map(location=[lat_c, lon_c], zoom_start=13)
    folium.Circle(
        location=[lat_c, lon_c],
        radius=radio_km * 1000,
        color='blue', weight=3, fill=False, opacity=0.5
    ).add_to(mapa)

    # 3) Haversine para distancia en km
    def _haversine(a_lat, a_lon, b_lat, b_lon):
        R = 6371.0
        φ1 = math.radians(a_lat)
        φ2 = math.radians(b_lat)
        dφ = math.radians(b_lat - a_lat)
        dλ = math.radians(b_lon - a_lon)
        a = math.sin(dφ/2)**2 + math.cos(φ1)*math.cos(φ2)*math.sin(dλ/2)**2
        return 2 * R * math.asin(math.sqrt(a))

    # 4) Filtrar vértices: que dp_id aparezca en info_lista y dentro del radio
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

    # 5) Si no hay puntos en la región, devolver None
    if lt.size(region) == 0:
        return None

    # 6) Dibujar marcadores verdes
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

    # 7) Dibujar ruta continua en rojo, en el orden de 'region'
    if lt.size(region) > 1:
        path = []
        for k in range(lt.size(region)):
            vid = lt.get_element(region, k)
            path.append(map.get(coords, vid))
        folium.PolyLine(locations=path, color='red', weight=3, opacity=0.8).add_to(mapa)

    # 8) Guardar HTML en Data/recorrido_domiciliario.html
    base = os.path.dirname(__file__)
    out_dir = os.path.abspath(os.path.join(base, '..', 'Data'))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'recorrido_domiciliario.html')
    mapa.save(out_path)

    return out_path  
    

