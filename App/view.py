"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapstructure as ht
assert cf
import datetime 


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar analizador")
    print("2- Cargar información en el catálogo")
    print("3- Contar los avistamientos en una ciudad")
    print("4- Contar los avistamientos por duración")
    print("5- Contar avistamientos por hora/minutos del día")
    print("6- Contar los avistamientos en un rango de fechas")
    print("7- Contar los avistamientos de una zona geográfica")
    print("8- Salir del programa")

catalog = None

def printAvista(avista): 
    print("+" + '-'*25 + '+' + '-'*16 +'+' + '-'*23 +'+' + '-'*12 +'+'+'-'*15+'+'+'-'*9+'+'+'-'*20+'+')
    datetimes = avista['datetime']
    dates = datetime.datetime.strptime(datetimes,'%Y-%m-%d %H:%M:%S')
    date = dates.date()
    strdate = datetime.datetime.strftime(date, "%Y-%m-%d")
    city = avista['city']
    state = avista['state']
    country = avista['country']
    shape = avista['shape']
    duration = avista['duration (seconds)']
    print(f"| {datetimes:24}| {strdate:15}| {city:22}| {state:11}| {country:14}| {shape:8}| {duration:19}| ")
    print("+" + '-'*25 + '+' + '-'*16 +'+' + '-'*23 +'+' + '-'*12 +'+'+'-'*15+'+'+'-'*9+'+'+'-'*20+'+')

def printAvistaZone(avista):
    datetimes = avista['datetime']
    dates = datetime.datetime.strptime(datetimes,'%Y-%m-%d %H:%M:%S')
    date = dates.date()
    strdate = datetime.datetime.strftime(date, "%Y-%m-%d")
    city = avista['city']
    state = avista['state']
    country = avista['country']
    shape = avista['shape']
    duration = avista['duration (seconds)']
    longitude = avista['longitude']
    latitude = avista['latitude']
    print(f"| {datetimes:24}| {strdate:15}| {city:22}| {state:11}| {country:14}| {shape:8}| {duration:19}| {longitude:10}| {latitude:10}| ")
    print("+" + '-'*25 + '+' + '-'*16 +'+' + '-'*23 +'+' + '-'*12 +'+'+'-'*15+'+'+'-'*9+'+'+'-'*20+'+'+'-'*10+'+'+"-"*10+"-"+'+')


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("\nInicializando....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de los archivos ....")
        datos = controller.loadData(cont)
        size = controller.avistaSize(cont)
        print('Avistamientos cargados: ' + str(size))

    elif int(inputs[0]) == 3:
        city = input("Ingresa la ciudad: ")
        datos = controller.countAvistabyCity(cont, city)
        size = lt.size(datos[1])
        print("El total de avistamientos en la ciudad seleccionada fue: " + str(size))
        print('Altura del árbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el árbol: ' + str(controller.indexSize(cont)))
        print('El total de ciudades es: ' + str(datos[0]))

        print("Los primeros tres elementos en el rango son: \n")
        print("+" + '-'*25 + '+' + '-'*16 +'+' + '-'*23 +'+' + '-'*12 +'+'+'-'*15+'+'+'-'*9+'+'+'-'*20+'+')
        print("| datetime\t\t  | date\t   | city\t\t   | state\t| country\t| shape\t  | duration (seconds) |" )
        i = 1 
        while i <=3 : 
            element = lt.getElement(datos[1],i)
            printAvista(element)
            i+=1 
        i = size  
        while i > size-3 : 
            element = lt.getElement(datos[1],i)
            printAvista(element)
            i-=1


    elif int(inputs[0]) == 6 : 
        fechaInicial = input("Ingrese la fecha inicial (AAAA-MM-DD): ")
        fechaFinal = input("Ingrese la fecha final (AAAA-MM-DD): ")
        prueba = controller.countAvista(cont,fechaInicial,fechaFinal)
        size = lt.size(prueba)
        print(f"El total de avistamientos entre las fechas seleccionadas fue: {size}")
       
        print("Los primeros tres elementos en el rango son: \n")
        print("+" + '-'*25 + '+' + '-'*16 +'+' + '-'*23 +'+' + '-'*12 +'+'+'-'*15+'+'+'-'*9+'+'+'-'*20+'+')
        print("| datetime\t\t  | date\t   | city\t\t   | state\t| country\t| shape\t  | duration (seconds) | longitude | latitude |" )
        i = 1 
        while i <=3 : 
            element = lt.getElement(prueba,i)
            printAvista(element)
            i+=1 
        i = size  
        while i > size-3 : 
            element = lt.getElement(prueba,i)
            printAvista(element)
            i-=1
    
    elif int(inputs[0]) == 7 :
        limitesLongitude = input("Ingrese el rango de longitudes a consultar (min,max) : ")
        limitesLatitude = input("Ingrese el rango de latitudes a consultar (min,max) : ") 
        datos = controller.countAvistabyZone(cont,limitesLongitude,limitesLatitude)
        size = lt.size(datos)
        print(f"El total de avistamientos dentro del area es: {size}")
        print("+" + '-'*25 + '+' + '-'*16 +'+' + '-'*23 +'+' + '-'*12 +'+'+'-'*15+'+'+'-'*9+'+'+'-'*20+'+')
        print("| datetime\t\t  | date\t   | city\t\t   | state\t| country\t| shape\t  | duration (seconds) | longitude | latitude |" )
        print("+" + '-'*25 + '+' + '-'*16 +'+' + '-'*23 +'+' + '-'*12 +'+'+'-'*15+'+'+'-'*9+'+'+'-'*20+'+')
        i = 1 
        while i <= 5 : 
            element = lt.getElement(datos,i)
            printAvistaZone(element)
            i += 1 
        i = size  
        while i > size-5 : 
            element = lt.getElement(datos,i)
            printAvistaZone(element)
            i -= 1       

    else:
        sys.exit(0)
sys.exit(0)
