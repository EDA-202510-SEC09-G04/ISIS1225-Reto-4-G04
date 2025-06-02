import sys
from App import logic as l
from time import time
from tabulate import tabulate 
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as map
from DataStructures.Graph import digraph as g
from DataStructures.Graph import dfs
from DataStructures.Graph import bfs
default_limit = 1000
sys.setrecursionlimit(default_limit*10)


def new_logic():
    logica = l.new_catalog()
    return logica


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8 (Bono)")
    print("0- Salir")

def load_data(control):
    carga = l.load_data(control,'deliverytime_100.csv')
    return carga


def print_req_1(control):
    ubicacion_A = input("Por favor escribe el punto donde se iniciara la busqueda: ")
    ubicacion_B = input("Por favor escribe el destino de la busqueda: ")
    print("\n" + "=" * 100 + "\n")
    tiempo_inical = time()
    conexion, grafo = l.req_1(control, ubicacion_A, ubicacion_B)
    tiempo_final = time() - tiempo_inical
    camino = dfs.pathTo(conexion, ubicacion_B)
    puntos = camino['size']
    print("Tiempo de ejecución:", tiempo_final)
    print("La cantidad de puntos geográficos en el camino son:", puntos,'\n')
    lista = []
    siguiente = camino['first']
    while siguiente != None:
        lista.append(siguiente['info'])
        siguiente = siguiente['next']
    secuencia = [camino]
    final = []
    domicilios = {}
    for direccion in lista:
        if direccion not in domicilios:
            domicilios[direccion] = map.get(grafo['vertices'], direccion)['elements']

    final.append(domicilios)
    print("El id de los domiciliarios que componen el camino son:", '\n', tabulate(final, headers = 'keys', tablefmt= 'fancy_grid'), '\n')
    print("La secuencia de ubicaciones que componene el camino simple son:", '\n',tabulate(secuencia, headers = 'keys', tablefmt= 'fancy_grid'), '\n') 
    print("Y el total de restaurantes encontrado son:", map.key_set(conexion['visited'])['elements'] )
    print("\n" + "=" * 100 + "\n")

def print_req_2(control):
    punto_a = input("Por favor escribe el punto donde se iniciara la busqueda: ")
    punto_b = input("Por favor escribe el destino de la busqueda: ")
    domiciliario = input("Por favor escriba el id del domiciliario: ")
    print("\n" + "=" * 100 + "\n")
    tiempo_inical = time()
    conexion, grafo = l.req_2(control, punto_a, punto_b,domiciliario)
    tiempo_final = time() - tiempo_inical
    camino = bfs.pathTo(conexion, punto_b)
    puntos = camino['size']
    print("Tiempo de ejecución:", tiempo_final)
    print("La cantidad de puntos geográficos en el camino son:", puntos,'\n')
    final = []
    domicilios = {}
    for direccion in camino['elements']:
        if direccion not in domicilios:
            domicilios[direccion] = map.get(grafo['vertices'], direccion)['elements']
    final.append(domicilios)
    print("El id de los domiciliarios que componen el camino son:", '\n', tabulate(final, headers = 'keys', tablefmt= 'fancy_grid'), '\n')
    print("La secuencia de ubicaciones que definen el camino simple son:", camino['elements'], '\n')
    print("Y el listado de restaurantes encontrado son:", map.key_set(conexion['visited'])['elements'])
    print("\n" + "=" * 100 + "\n")
    
    
    



def print_req_3(control):

    geo_point = input("Por favor, escribe el punto geográfico para consultar: ")
    print("\n" + "=" * 100 + "\n")

    # Medir tiempo de ejecución
    inicio = time()
    dp_id, total_pedidos, vehiculo_favorito = l.req_3(control, geo_point)
    duracion = time() - inicio

    print(f"Tiempo de ejecución: {duracion:.6f} s\n")

    if dp_id is None:
        print("No se encontraron pedidos en el punto consultado.")
    else:
        # Mostrar resultados en tabla
        resultados = [{
            'Domiciliario': dp_id,
            'Pedidos': total_pedidos,
            'Vehículo más usado': vehiculo_favorito
        }]
        print(tabulate(resultados, headers='keys', tablefmt='fancy_grid'))

    print("\n" + "=" * 100 + "\n")


def print_req_4(control):
    punto_a = input("Por favor escribe el punto donde se iniciara la busqueda: ")
    punto_b = input("Por favor escribe el destino de la busqueda: ")
    print("\n" + "=" * 100 + "\n")
    tiempo_inical = time()
    secuencia, lista= l.req_4(control,punto_a,punto_b)
    tiempo_final = time() - tiempo_inical
    print("Tiempo de ejecución:", tiempo_final)
    print("La secuencia de ubicaciones entre los dos puntos son:", secuencia)
    print("El listado de domiciliarios en comun para ESE CAMINO son:", lista)
    print("\n" + "=" * 100 + "\n")
    
    
    



def print_req_5(control):
    """
    Vista para el Requerimiento 5:
    Pide punto geográfico inicial y número N de cambios,
    llama a l.req_5, mide el tiempo y muestra los resultados.
    """
    print("\n" + "=" * 100)
    print("Requerimiento 5: Identificar el domiciliario que recorre mayor distancia en N cambios")
    print("=" * 100 + "\n")

    punto_inicial_id = input("Por favor, escribe el ID del punto geográfico inicial (e.g., 'Latitud_Longitud'): ")
    try:
        N_cambios = int(input("Por favor, escribe el número N de cambios de ubicación a consultar: "))
        if N_cambios < 0:
            print("El número N de cambios no puede ser negativo.")
            print("\n" + "=" * 100 + "\n")
            return
    except ValueError:
        print("Número N de cambios inválido. Debe ser un entero.")
        print("\n" + "=" * 100 + "\n")
        return

    print("\nCalculando...\n")

    # Llamar a la función lógica y medir el tiempo
    # Se asume que req_5 devuelve: domiciliario_id, max_distancia, camino_secuencia, tiempo_ejecucion_logica
    # Nota: La función req_5 que te di anteriormente ya calcula su propio tiempo, así que podemos usar ese directamente.
    
    domiciliario_id, max_distancia, camino_secuencia_lista, duracion = l.req_5(control, punto_inicial_id, N_cambios)

    print(f"Tiempo de ejecución del requerimiento: {duracion:.6f} segundos.\n")

    if domiciliario_id is None:
        print(f"No se encontró ningún domiciliario o camino válido para {N_cambios} cambios desde {punto_inicial_id}.")
    else:
        # Preparar datos para tabulate
        resultados_domiciliario = [
            {"Variable": "ID Domiciliario con Mayor Distancia", "Valor": domiciliario_id},
            {"Variable": "Mayor Distancia Recorrida (km)", "Valor": f"{max_distancia:.4f} km"}
        ]
        
        # Convertir la lista de secuencia de camino a un formato imprimible
        camino_str_list = []
        if camino_secuencia_lista is not None and camino_secuencia_lista['size'] > 0: # Usando la estructura de tu array_list
            current = camino_secuencia_lista['first']
            while current is not None:
                camino_str_list.append(str(current['info']))
                current = current['next']
        
        secuencia_imprimible = " -> ".join(camino_str_list) if camino_str_list else "No disponible"

        print(tabulate(resultados_domiciliario, headers="keys", tablefmt="fancy_grid"))
        print("\nSecuencia de ubicaciones del camino de mayor distancia:")
        print(secuencia_imprimible)

    print("\n" + "=" * 100 + "\n")



def print_req_6(control):
    punto_a = input("Por favor escribe el punto donde se iniciara la busqueda: ")
    print("\n" + "=" * 100 + "\n")
    tiempo_inical = time()
    numero_ubic_alcanzables,id_alcanzables_sort, secuencia_mayor_tiempo, max_tiempo = l.req_6(control,punto_a)
    tiempo_final = time() - tiempo_inical
    print("Tiempo de ejecución:", tiempo_final)
    print("La cantidad de ubicaciones que definen los caminos de c/m son:", numero_ubic_alcanzables,'\n')
    print("Los ids de las ubicaciones alcanzables ordenados alfabeticamente son:", id_alcanzables_sort['elements'],'\n')
    print("El camino de costo minimo desde", punto_a, "que implica mayor tiempo es:", 'Secuencia:', secuencia_mayor_tiempo['first'],'\n','\n' 'Tiempo:', max_tiempo)
    print("\n" + "=" * 100 + "\n")


def print_req_7(control):
    punto_a = input("Por favor escribe el punto donde se iniciara la busqueda: ")
    domiciliario = input("Por favor escriba el id del domiciliario:")
    print("\n" + "=" * 100 + "\n")
    tiempo_inical = time()
    resp = l.req_7(control,punto_a,domiciliario)
    tiempo_final = time() - tiempo_inical
    print("Tiempo de ejecución:", tiempo_final)
    print("La cantidad de ubicaciones que definen la subred, son:",resp['cantidad_ubicaciones_subred'],'\n')
    print("Los ids que componen la subred alfabeticamente son:", resp['identificadores_subred_ordenados']['elements'], '\n')
    print("El total en tiempo del arbol en costo minimo es:", resp['peso_total_mst'])
    print("\n" + "=" * 100 + "\n")


def print_req_8(control):
    """
    Vista para el Requerimiento 8:
    Pide punto central, radio y ID de domiciliario,
    llama a l.req_8, mide el tiempo y muestra la ruta al HTML generado.
    """
    centro = input("Por favor, escribe el punto central: ")
    radio = float(input("Por favor, escribe el radio en kilómetros: "))
    dp_id = input("Por favor, escribe el ID del domiciliario: ")
    print("\n" + "=" * 100 + "\n")

    inicio = time()
    ruta_html = l.req_8(control, centro, radio, dp_id)
    duracion = time() - inicio

    print(f"Tiempo de ejecución: {duracion:.6f} s\n")
    print(f"Mapa generado en: {ruta_html}")
    print("Ábrelo en tu navegador para visualizar el recorrido.\n")

    print("=" * 100 + "\n")
# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("=" * 100)
            print("Cargando información de los archivos ....\n")
            tiempo_inicial = time()
            catalog, domicilios_procesados, total_tiempo_entregas = load_data(control)
            tiempo_final = time() - tiempo_inicial
            print("¡Información cargada con éxito!\n")
            print("=" * 100)
            print("Tiempo de ejecución:", tiempo_final,'\n')
            print("1. El numero total de domicilios procesados son:", domicilios_procesados)
            print("2. El numero total de domiciliarios identificados son:", map.size(catalog['ultimo_domicilio_persona']))
            print("3. El numero total de nodos en el grafo creado son:", g.order(catalog['grafo_domicilios']))
            print("4. El numero de Arcos en el grafo son:", int(g.size(catalog['grafo_domicilios'])))
            print("5. El numero de restaurantes unicos identificados son: ", map.size(catalog['ubicaciones_restaurantes_unicas']))
            print("6. El numero de ubicaciones de entrega unicas son: ", map.size(catalog['ubicaciones_destino_unicas']))
            print('7. el tiempo promedio de entrega de todos los domicilios es: ' + str(total_tiempo_entregas / domicilios_procesados) + ' minutos')
            print("\n" + "=" * 100 + "\n")
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
