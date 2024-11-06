"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

import config as cf
from App import logic
import csv
import time





# ___________________________________________________
#  Importaciones
# ___________________________________________________

from DataStructures.Graph import adj_list_graph as gr
from DataStructures.Map import map_linear_probing as m
from DataStructures.List import single_linked_list as lt
"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = newAnalyzer()
    return analyzer

def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
            'stops': None,
            'connections': None,
            'components': None,
            'paths': None
        }

        analyzer['stops'] = m.new_map(num_elements=14000,load_factor=0.7,prime=109345121) 

        analyzer['connections'] = gr.new_graph(size=14000,directed=False)
        return analyzer
    except Exception as exp:
        return exp

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadServices(analyzer, servicesfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    servicesfile = cf.data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    lastservice = None
    for service in input_file:
        if lastservice is not None:
            sameservice = lastservice['ServiceNo'] == service['ServiceNo']
            samedirection = lastservice['Direction'] == service['Direction']
            samebusStop = lastservice['BusStopCode'] == service['BusStopCode']
            if sameservice and samedirection and not samebusStop:
                addStopConnection(analyzer, lastservice, service)
        lastservice = service
  
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________


def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return logic.totalStops(analyzer)
     

def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return logic.totalConnections(analyzer)
     


def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    start_time = getTime()
    connected_components = logic.connectedComponents(analyzer)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    return delta_time, connected_components


def minimumCostPaths(analyzer, initialStation):
    """
    Calcula todos los caminos de costo minimo de initialStation a todas
    las otras estaciones del sistema
    """
    start_time = getTime()
    minimum_costh_paths = logic.minimumCostPaths(analyzer, initialStation)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    return delta_time, minimum_costh_paths


def hasPath(analyzer, destStation):
    """
    Informa si existe un camino entre initialStation y destStation
    """
    start_time = getTime()
    has_path = logic.hasPath(analyzer, destStation)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    return delta_time, has_path


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    start_time = getTime()
    minimum_costh_path = logic.minimumCostPath(analyzer, destStation)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    return delta_time, minimum_costh_path


def servedRoutes(analyzer):
    """
    Retorna el camino de costo minimo desde initialStation a destStation
    """
    start_time = getTime()
    maxvert, maxdeg = logic.servedRoutes(analyzer)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    return delta_time, maxvert, maxdeg
    

#Funciones para la medición de tiempos

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para agregar informacion al grafo

def addStopConnection(analyzer, lastservice, service):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origin = formatVertex(lastservice)
        destination = formatVertex(service)
        cleanServiceDistance(lastservice, service)
        distance = float(service['Distance']) - float(lastservice['Distance'])
        distance = abs(distance)
        addStop(analyzer, origin)
        addStop(analyzer, destination)
        addConnection(analyzer, origin, destination, distance)
        addRouteStop(analyzer, service)
        addRouteStop(analyzer, lastservice)
        return analyzer
    except Exception as exp:
        return exp

def addStop(analyzer, stopid):
    """
    Adiciona una estación como un vertice del grafo
    """
 
      
    gr.insert_vertex(analyzer['connections'], stopid,stopid)
    return analyzer



def addRouteStop(analyzer, service):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    entry = m.get(analyzer['stops'], service['BusStopCode'])
    if entry is None:
        lstroutes = lt.new_list()
        lt.add_last(lstroutes, service['ServiceNo'])
        m.put(analyzer['stops'], service['BusStopCode'], lstroutes)
    else:
        lstroutes = entry['value']
        info = service['ServiceNo']
        if not lt.is_present(lstroutes, info):
            lt.add_last(lstroutes, info)
    return analyzer


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
   
    gr.add_edge(analyzer['connections'], origin, destination, distance)
 



# ==============================
# Funciones Helper
# ==============================

def cleanServiceDistance(lastservice, service):
    """
    En caso de que el archivo tenga un espacio en la
    distancia, se reemplaza con cero.
    """
    if service['Distance'] == '':
        service['Distance'] = 0
    if lastservice['Distance'] == '':
        lastservice['Distance'] = 0


def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['BusStopCode'] + '-'
    name = name + service['ServiceNo']
    return name


