"""
 * Copyright 2020, Departamento de sistemas y Computación,
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    analyzer = {'avista': None,
                'datetime': None
                }

    analyzer['avista'] = lt.newList('SINGLE_LINKED')
    analyzer['datetime'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer

# Funciones para agregar informacion al catalogo

def addAvista(analyzer, avista):
    lt.addLast(analyzer['avista'], avista)
    updateDateIndex(analyzer['datetime'], avista)
    return analyzer


def updateDateIndex(map, avista):
    date = avista['datetime']
    avistadate = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, avistadate.date())
    if entry is None:
        datentry = newDataEntry(avista)
        om.put(map, avistadate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, avista)
    return map


def addDateIndex(datentry, avista):
    lst = datentry['lstavista']
    lt.addLast(lst, avista)
    avistaIndex = datentry['avistaIndex']
    avistaentry = m.get(avistaIndex, avista['city'])
    if (avistaentry is None):
        entry = newCityEntry(avista['city'], avista)
        lt.addLast(entry['lstcities'], avista)
        m.put(avistaIndex, avista['city'], entry)
    else:
        entry = me.getValue(avistaentry)
        lt.addLast(entry['lstcities'], avista)
    return datentry


# Funciones para creacion de datos

def newDataEntry(avista):
    entry = {'avistaIndex': None, 'lstavista': None}
    entry['avistaIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareCities)
    entry['lstavista'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def newCityEntry(city, avista):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'city': None, 'lstcities': None}
    ofentry['city'] = city
    ofentry['lstcities'] = lt.newList('SINGLELINKED', compareCities)
    return ofentry

# Funciones de consulta

def avistaSize(analyzer):
    return lt.size(analyzer['avista'])

# Funciones utilizadas para comparar elementos dentro de una lista

def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareCities(city1, city2):
    """
    Compara dos tipos de crimenes
    """
    city = me.getKey(city2)
    if (city1 == city):
        return 0
    elif (city1 > city):
        return 1
    else:
        return -1

# Funciones de ordenamiento
