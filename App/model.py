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
import sys
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mer
from DISClib.ADT import orderedmap as om
import datetime
assert cf
sys.setrecursionlimit(10**6)

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    analyzer = {'avista': None,
                'city': None,
                'datetime': None,
                'duration (seconds)': None
                }

    analyzer['avista'] = lt.newList('SINGLE_LINKED')
    analyzer['city'] = om.newMap(omaptype='RBT',
                                comparefunction=compareCities)
    analyzer['datetime'] = om.newMap(omaptype='RBT',
                                comparefunction=compareDates)
    analyzer['duration (seconds)'] = om.newMap(omaptype='RBT',
                                comparefunction= compareDurations)
    analyzer['longitude'] = om.newMap(omaptype='RBT',
                                comparefunction= compareLongitudes)
    
    
            
    
    return analyzer

# Funciones para agregar informacion al catalogo

def addAvista(analyzer, avista):
    lt.addLast(analyzer['avista'], avista)
    updateDateIndex(analyzer['datetime'], avista)
    updateDurationIndex(analyzer['duration (seconds)'],avista)
    upCityIndex(analyzer['city'], avista)
    updateLongitudeIndex(analyzer['longitude'],avista)
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

def updateLongitudeIndex(map,avista):
    longitude = round(float(avista['longitude']),2)
    entry = om.get(map,longitude)
    if entry is None : 
        longitudeEntry = newLongitudeEntry(avista)
        om.put(map,longitude,longitudeEntry)
    else : 
        longitudeEntry = me.getValue(entry)
    addLongitudeIndex(longitudeEntry,avista)
    return map 

def updateDurationIndex(map,avista):
    duration = avista['duration (seconds)']
    entry = om.get(map,duration)
    if entry is None : 
        durationEntry = newDurationEntry(avista)
        om.put(map,duration,durationEntry)
    else : 
        durationEntry = me.getValue(entry)
    addDurationIndex(durationEntry,avista)
    return map 

def addDateIndex(datentry, avista):
    lst = datentry['lstavista']
    lt.addLast(lst, avista)

def addDurationIndex(durationEntry,avista) : 
    lst = durationEntry['lstAvista']
    lt.addLast(lst,avista)

def addLongitudeIndex(longitudeEntry,avista) :
    lst = longitudeEntry['lstAvista']
    lt.addLast(lst,avista)

def upCityIndex(map, avista):
    city = avista['city']
    entry = om.get(map, city)
    if entry is None:
        cityentry = newDataEntry(avista)
        om.put(map, city, cityentry)
    else:
        cityentry = me.getValue(entry)
    addCityIndex(cityentry, avista)
    return map


def addCityIndex(cityentry, avista):
    lst = cityentry['lstavista']
    lt.addLast(lst, avista)



# Funciones para creacion de datos

def newDataEntry(avista):
    entry = {'avistaIndex': None, 'lstavista': None}
    entry['avistaIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareCities)
    entry['lstavista'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newDurationEntry(avista) : 
    entry = {'avistaDuration': None, 'lstAvista': None}
    entry['avistaIndex'] = m.newMap(numelements=30,
                                        maptype='PROBING',
                                        comparefunction=compareDurations)
    entry['lstAvista'] = lt.newList('SINGLE_LINKED',compareDurations)
    return entry 

def newLongitudeEntry(avista) : 
    entry = {'lstAvista': None}
    entry['lstAvista'] = lt.newList('SINGLE_LINKED',compareDurations)
    return entry 

def newDurationEntry_2(duration,avista) : 
    entry = {'avistaDuration': None, 'lstAvista':None}
    entry['avistaDuration'] = duration
    entry['lstavista'] = lt.newList('SINGLELINKED',compareDurations)
    return entry  

def newCityEntry():
    cityentry = {'lstcities': None}
    cityentry['lstcities'] = lt.newList('SINGLELINKED', compareCities)
    return cityentry

# Funciones de consulta

def avistaSize(analyzer):
    return lt.size(analyzer['avista'])

def indexHeight(analyzer):
    return om.height(analyzer['datetime'])


def indexSize(analyzer):
    return om.size(analyzer['datetime'])

#FUNCION REQUERIMIENTO 1 

def countAvistabyCity(analyzer, city):
    cities = om.size(analyzer['city'])
    valor = om.get(analyzer['city'],city)
    avistaCity = me.getValue(valor)['lstavista']
    mer.sort(avistaCity,compareDateTime)
    return cities,avistaCity

#FUNCION REQUERIMIENTO 2 

def countAvistabyDuration (analyzer,limInferior,limSuperior) : 
    keyMayor = om.maxKey(analyzer['duration (seconds)'])
    mayores = om.get(analyzer['duration (seconds)'],keyMayor)
    listmayores = lt.newList('ARRAY_LIST')
    value = me.getValue(mayores)
    for element in lt.iterator(value['lstAvista']) : 
        lt.addLast(listmayores,element)
    valoresRango = om.values(analyzer['duration (seconds)'],limInferior,limSuperior)
    listValores = lt.newList('ARRAY_LIST')
    for element in lt.iterator(valoresRango):
        avistam =  element['lstAvista']
        if lt.size(avistam) > 1 : 
            mer.sort(avistam,compareCountrycity)
            for avista in lt.iterator(element['lstAvista']) : 
                lt.addLast(listValores,avista)
        else : 
            avista = lt.getElement(element['lstAvista'],1)
            lt.addLast(listValores,avista)
    return lt.size(listmayores), listValores
        
#FUNCIÓN REQUERIMIENTO 3

def countAvistabyHour(analyzer,horaInicial,horaFinal) : 
    valores = om.values(analyzer['datetime'],horaInicial,horaFinal)
    avista = lt.newList('ARRAY_LIST')
    i = 1
    while i <= lt.size(valores): 
        value = lt.getElement(valores,i)
        for element in lt.iterator(value['lstavista']) : 
            lt.addLast(avista,element)
        i += 1 
    mer.sort(avista,compareDateTime)
    return avista



#FUNCION REQUERIMIENTO 4 

def countAvistabyDate(analyzer,fechaInicial,fechaFinal) : 
    valores = om.values(analyzer['datetime'],fechaInicial,fechaFinal)
    avista = lt.newList('ARRAY_LIST')
    i = 1
    while i <= lt.size(valores) : 
        value = lt.getElement(valores,i)
        for element in lt.iterator(value['lstavista']) : 
            lt.addLast(avista,element)
        i += 1 
    mer.sort(avista,compareDateTime)
    return avista



#FUNCION REQUERIMIENTO 5 

def countAvistabyZone(analyzer,limitesLong,limitesLat) : 
    listLimitesLong = limitesLong.split(',')
    listLimitesLat = limitesLat.split(',')
    listAvistaLat = om.values(analyzer['longitude'],float(listLimitesLong[0]),float(listLimitesLong[1])) 
    avistaLat = lt.newList('ARRAY_LIST')
    for lista in lt.iterator(listAvistaLat) : 
        for element in lt.iterator(lista['lstAvista']) :
            lt.addLast(avistaLat,element)
    mer.sort(avistaLat,compareLatitude)
    avista = lt.newList('ARRAY_LIST')
    for element in lt.iterator(avistaLat) : 
        if round(float(element['latitude']),2) >= float(listLimitesLat[0]) and round(float(element['latitude']),2) < float(listLimitesLat[1]) : 
            lt.addLast(avista,element) 
        elif element['latitude'] == listLimitesLat[1] : 
            lt.addLast(avista,element)
            break
    return avista 




# Funciones utilizadas para comparar elementos dentro de una lista
def compareDateTime (elem1,elem2) : 
    date_1 =  datetime.datetime.strptime(elem1['datetime'],'%Y-%m-%d %H:%M:%S')
    date_2 =  datetime.datetime.strptime(elem2['datetime'],'%Y-%m-%d %H:%M:%S')
    return date_1 < date_2

def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareDuration(elem1,elem2) : 
    duration_1 = float(elem1['duration (seconds)'])
    duration_2 = float(elem2['duration (seconds)'])
    return duration_1 < duration_2

def compareDurations(duration1,duration2): 
    if (float(duration1) == float(duration2)) : 
        return 0 
    elif (float(duration1) > float(duration2)) : 
        return 1
    else: 
        return -1 

def compareCities(city1, city2):
    if (city1 == city2):
        return 0
    elif (city1 > city2):
        return 1
    else:
        return -1
def compareCity(elem1,elem2): 
    city1 = elem1['city']
    city2 = elem2['city']
    return city1 < city2

def compareLongitudes(longitude1, longitude2):
    if (longitude1 == longitude2):
        return 0
    elif (longitude1 > longitude2):
        return 1
    else:
        return -1

def compareLongitude(elem1,elem2) : 
    long1 = elem1['longitude']
    long2 = elem2['longitude']
    return long1 < long2

def compareLatitude(elem1,elem2) :
    lat1 = elem1['latitude']
    lat2 = elem2['latitude']
    return lat1 < lat2

def compareCountrycity(elem1,elem2) : 
    countryCity_1 = elem1['country'].lower() + "-" + elem1['city'].lower().strip(' ') 
    countryCity_2 = elem2['country'].lower() + "-" + elem2['city'].lower().strip(' ') 
    return countryCity_1 < countryCity_2 


# Funciones de ordenamiento
