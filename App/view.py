import sys
from App import logic
from tabulate import tabulate


def new_logic():
    """
        Se crea una instancia del controlador
    """
    control = logic.new_logic()
    return control

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
    """
    Carga los datos
    """
    catalog, total_domicilios, total_domiciliarios, total_nodos, total_arcos, restaurantes, destinos, total_tiempo, delta = logic.load_data(control)

    return catalog, total_domicilios, total_domiciliarios, total_nodos, total_arcos, restaurantes, destinos, total_tiempo, delta 

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    fecha = input("Ingrese la fecha (YYYY-MM-DD): ")
    r = logic.req_1(control, fecha)
    print(f"\nTiempo de ejecución: {r['tiempo_ms']} ms")
    print(f"Cantidad de entregas: {r['total_entregas']}")
    print(tabulate(r['tabla'], headers="keys", tablefmt="fancy_grid"))

def print_req_2(control):
    ini = input("Unbicaciòn A: ")
    fin = input("Ubicaciòn B: ")
    id = input("ID del domiciliario: ")
    r = logic.req_2(control, id,ini, fin)
    print(f"\nTiempo de ejecución: {r['tiempo_en_ms']} ms")
    print(f"Total entregas: {r}")
    # print(tabulate(r['tabla'], headers="keys", tablefmt="fancy_grid"))

def print_req_3(control):
    origen = input("Ubicación origen (lat_long): ")
    r = logic.req_3(control, origen)
    print(f"\nTiempo de ejecución: {r['tiempo_ms']} ms")
    print(f"Cantidad de paquetes entregados: {r['cantidad']}")
    print(tabulate(r['tabla'], headers="keys", tablefmt="fancy_grid"))

def print_req_4(control):
    punto_a = input("Punto A (lat_long): ")
    punto_b = input("Punto B (lat_long): ")
    r = logic.req_4(control, punto_a, punto_b)
    print(f"\nTiempo de ejecución: {r['tiempo_ms']} ms")
    print("Ruta más rápida:")
    print(tabulate(r['ruta'], headers=['#', 'Ubicación'], tablefmt="fancy_grid"))
    print(f"Tiempo total: {r['tiempo_total']} s")

def print_req_5(control):
    r = logic.req_5(control)
    print(f"\nTiempo de ejecución: {r['tiempo_ms']} ms")
    print(f"Total componentes fuertemente conectados: {r['total_componentes']}")
    print(tabulate(r['conexiones'], headers=['Componente', 'Tamaño'], tablefmt="fancy_grid"))

def print_req_6(control):
    origen = input("Ubicación origen (lat_long): ")
    r = logic.req_6(control, origen)
    print(f"\nTiempo de ejecución: {r['tiempo_ms']} ms")
    print(f"Ubicaciones alcanzables: {r['cantidad_ubicaciones']}")
    tabla = [[i+1, u] for i, u in enumerate(r['ubicaciones'])]
    print(tabulate(tabla, headers=['#', 'Ubicación'], tablefmt='fancy_grid'))
    camino = r['camino_mas_costoso']
    print("\nCamino más costoso:")
    print(f"Destino: {camino['destino']}, Tiempo: {camino['tiempo_total']} s")
    secuencia = [[i+1, paso] for i, paso in enumerate(camino['secuencia'])]
    print(tabulate(secuencia, headers=['#', 'Paso'], tablefmt='fancy_grid'))

def print_req_7(control):
    origen = input("Ubicación origen (lat_long): ")
    dom = input("ID del domiciliario: ")
    r = logic.req_7(control, origen, dom)
    print(f"\nTiempo de ejecución: {r['tiempo_ms']} ms")
    print(f"Cantidad de ubicaciones en MST: {r['cantidad_ubicaciones']}")
    tabla = [[i+1, u] for i, u in enumerate(r['ubicaciones'])]
    print(tabulate(tabla, headers=['#', 'Ubicación'], tablefmt='fancy_grid'))
    print(f"Costo total del árbol: {r['tiempo_total']} s")


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    print('generando mapa...')
    
    return logic.req_8(control)
    


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
            print("Cargando información de los archivos ....\n")
            catalog, total_domicilios, total_domiciliarios, total_nodos, total_arcos, restaurantes, destinos, total_tiempo, delta = load_data(control)
            print("🗂️ Catálogo cargado:", "Sí" if catalog else "No")
            print("📦  Total de domicilios:", total_domicilios)
            print("🚴‍♂️  Total de domiciliarios:", total_domiciliarios)
            print("🧩  Total de nodos:", total_nodos)
            print("🔗  Total de arcos:", total_arcos)
            print("🍽️  Cantidad de restaurantes:", restaurantes)
            print("📍  Cantidad de destinos:", destinos)
            print("⏱️  Tiempo total de procesamiento:", total_tiempo, "segundos")
            print("⏳  Delta de tiempo (carga):", delta, "milisegundos")
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
