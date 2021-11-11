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
 """

import config as cf
import model
import csv
import datetime 


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de avistamientos

def init():
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer):
    avistafile = cf.data_dir + 'UFOS-utf8-small.csv'
    input_file = csv.DictReader(open(avistafile, encoding="utf-8"),
                                delimiter=",")
    for avista in input_file:
        model.addAvista(analyzer, avista)
    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def avistaSize(analyzer):
    return model.avistaSize(analyzer)

def indexHeight(analyzer):
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    return model.indexSize(analyzer)

def countAvistabyHour(analyzer,hourInicial,hourFinal):
    return model.countAvistabyHour(analyzer,hourInicial,hourFinal)

def countAvista(analyzer,fechaInicial,fechaFinal) :
    fecha_1 = datetime.date.fromisoformat(fechaInicial)
    fecha_2 = datetime.date.fromisoformat(fechaFinal)
    return model.countAvistabyDate(analyzer,fecha_1,fecha_2)

def countAvistabyZone(analyzer,limitesLong,limitesLat) : 
    return model.countAvistabyZone(analyzer,limitesLong,limitesLat)

def countAvistabyCity(analyzer, city):
    return model.countAvistabyCity(analyzer, city)
