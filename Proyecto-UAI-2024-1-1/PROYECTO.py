#Manuel Lorenzo
#Cristobal Garcia
#Alexander Frings
#Alonso Arevalo 
#Seccion: 10

import random
from jugada_cpu import jugada_cpu
import pygame
import time
pygame.init()
ancho = 800
alto = 800
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Proyecto")

def cerrar():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
def mostrar_tablero(ventana, tablero):
    ventana.fill((255, 255, 255))  # Rellena la ventana con color blanco
    tamaño_celda = ancho // TAMAÑO  # Calcula el tamaño de cada celda
    
    for fila in range(TAMAÑO):
        for columna in range(TAMAÑO):
            rect = pygame.Rect(columna * tamaño_celda, fila * tamaño_celda, tamaño_celda, tamaño_celda) #Crea graficamente las celdas
            if tablero[fila][columna] == BLANCO:
                color = (0, 255, 255)  # celeste
            elif tablero[fila][columna] == NEGRO:
                color = (0, 0, 0)  # Negro
            elif tablero[fila][columna] == BLOQUEADO:
                color = (255, 0, 0)  # rojo
            else:
                color = (255, 225, 255)  # Blanco para celdas vacías
            pygame.draw.rect(ventana, color, rect)
            pygame.draw.rect(ventana, (0, 0, 0), rect, 1)  # Borde negro alrededor de cada celda
    pygame.display.flip()  # Actualiza la pantalla


# Valores que representan las distintas jugadas
VACIO = 0
BLANCO = 1
NEGRO = -1
BLOQUEADO = 2
CPU = NEGRO # Color asignado a la computadora

TAMAÑO = 8 # Tamaño del tablero (8x8 por defecto)
CELDAS_BLOQUEADAS = 8 # Cantidad de celdas a bloquear
RONDAS = 1000# Cantidad de rondas a jugar (Cambiar a 1000 para el reporte final)

# Configuración del despliegue en terminal
MOSTRAR_TERMINAL = True #Mostrar juego en terminal
NOMBRE_COLUMNAS = "ABCEDFGHIJKL"[:TAMAÑO]
NOMBRE_FILAS = list(range(1,TAMAÑO + 1))
for i in range(len(NOMBRE_FILAS)):
    NOMBRE_FILAS[i] = str(NOMBRE_FILAS[i])

# Genera un tablero de TAMAÑOxTAMAÑO con CELDAS_BLOQUEADAS cantidad de celdas bloqueadas en lugares aleatorios.
def inicializar_tablero():
    tablero = []
    for _ in range(TAMAÑO):
        fila = []
        for _ in range(TAMAÑO):
            fila.append(VACIO)
        tablero.append(fila)
    for _ in range(CELDAS_BLOQUEADAS):
        fila_aleatoria = random.randint(0,TAMAÑO - 1)
        columna_aleatoria = random.randint(0,TAMAÑO - 1)
        while tablero[fila_aleatoria][columna_aleatoria] != VACIO:
            fila_aleatoria = random.randint(0,TAMAÑO - 1)
            columna_aleatoria = random.randint(0,TAMAÑO - 1)
        else:
            tablero[fila_aleatoria][columna_aleatoria] = BLOQUEADO
    return tablero




# Revisa la validad de la jugada en base a las reglas del juego (la celda debe estar vacia)
def jugada_es_valida(tablero, fila, columna):
    if tablero[fila][columna] == VACIO :
        return True
    return False

# Genera una lista bidimensional con todas las casillas disponibles donde hay jugadas validas    
def obtener_jugadas_validas(tablero):
    jugadas_validas = []
    for fila in range(TAMAÑO):
        for columna in range(TAMAÑO):
            if jugada_es_valida(tablero, fila, columna):
                jugadas_validas.append([fila, columna])
    return jugadas_validas

# Logíca para cambiar las fichas en base a las reglas del juego (cuando el jugador encierra fichas del oponente entre sus fichas)
def cambiar_fichas(tablero, fila, columna, jugador):
    # Se definen las 8 direcciones donde se pueden cambiar fichas
    direcciones = [
        [-1, -1], [-1, 0], [-1, 1],
        [ 0, -1], [ 0, 0], [ 0, 1],
        [ 1, -1], [ 1, 0], [ 1, 1],
    ]

    oponente = -jugador

    for cambio_fila, cambio_columna in direcciones:
        fila_actual = fila + cambio_fila
        columna_actual = columna + cambio_columna
        fichas_a_cambiar = []

        while 0 <= fila_actual < TAMAÑO and 0 <= columna_actual < TAMAÑO and tablero[fila_actual][columna_actual] == oponente:
            fichas_a_cambiar.append([fila_actual, columna_actual])
            fila_actual += cambio_fila
            columna_actual += cambio_columna

        if 0 <= fila_actual < TAMAÑO and 0 <= columna_actual < TAMAÑO and tablero[fila_actual][columna_actual] == jugador:
            for fila, columna in fichas_a_cambiar:
                tablero[fila][columna] = jugador

# Actualizar el tablero en base a la jugada
def realizar_jugada(tablero, fila, columna, jugador):
    tablero[fila][columna] = jugador
    cambiar_fichas(tablero, fila, columna, jugador)

# Código para rellenar esquinas
def marcar_esquinas(tablero):
    vacio = 0

    if tablero[0][0] == vacio:    #Revisa si la esquina 0,0 esta vacia , de ser asi lo ocupa
        return 0,0
    
    if tablero[0][7] == vacio:      #Revisa si la esquina 0,7 esta vacia , de ser asi lo ocupa
        return 0,7   

    if tablero[7][0] == vacio:   #Revisa si la esquina 7,0 esta vacia , de ser asi lo ocupa
        return 7,0

    if tablero[7][7] == vacio:    #Revisa si la esquina 7,7 esta vacia , de ser asi lo ocupa
        return 7,7

# Código para rellenar bordes
def rellenar_bordes(tablero):
    if tablero[0][0]== 1:     #borde superior partiendo de 0,0 hacia la derecha
        for x in range(1,7,1):
            if tablero[0][x] == 0:
                return [0, x] 
    if tablero[0][0]== 1:       #borde izquierdo partiendo de 0,0 hacia abajo
        for x in range(1,7,1):
            if tablero[x][0] == 0:
                return [x, 0]         
    if tablero[0][7]== 1:     #borde superior partiendo de 0,7 hacia la izquierda
        for x in range(6,-1,-1):
            if tablero[7][x] == 0:
                return [7, x]     
    if tablero[0][7] == 1:    #borde derecho partiendo de 0,7 hacia abajo  
        for x in range(1, TAMAÑO - 1):
            if tablero[x][7]==0:
                return[x,7]
    if tablero[7][0]==1:         #borde inferior partiendo de 7,0    hacia la derecha
        for x in range(1, TAMAÑO - 1):
            if tablero[7][x]==0:
                return[7,x]
    elif tablero[7][0]==1 :       #bordes izquierdo partiendo en 7,0     hacia arriba
        for x in range(6,-1,-1):
            if tablero[x][0]==0:
                return[ x , 0]
    if tablero[7][7]== 1:           #borde inferiore izquierdo partiendo de 7,7  hacia la izquierda
        for x in range(6,-1,-1):
            if tablero[7][x] == 0:
                return [7, x] 
    if tablero[7][7]== 1:          #borde derecho partiendo en 7,7    hacia arriba
        for x in range(6,-1,-1):
            if tablero[x][7]==0:
                return[ x , 7]
         
#listaespacios que proviene de la funcion rellenar_espacios
def Alrededor_de_Equis(tablero):
    lista = []
    for i in range(len(tablero)):        # i: Recorre números del tablero 
        for x in range(len(tablero[i])):  # x: Recorre letras del tablero
            if tablero[i][x] == 2:        #almacenara informacion de las celdas bloqueadas
                Listaequis = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # esos ceros vacíos luego se rellenan con cada dato [[Coordenada y][Coordenada x][Espacios disponibles a su derecha][ Espacios disponibles a su izquierda][ Espacios disponibles a abajo][ Espacios disponibles a  arriba][ Espacios disponibles a 45 grados, sentido derecha][ Espacios disponibles a 45 grados , sentido izquierda][ Espacios disponibles a 135 grados, sentido izquierda][ Espacios disponibles a 135 grados, sentido derecha]]
                Listaequis[0] = i  # dejar guardada en la lista la posición de la y
                Listaequis[1] = x  # dejar guardada en la lista la posición de la X  
                
                derecha = 0  # contador de ceros a la derecha
                for j in range(x + 1, len(tablero[i])):  # Revisa cuantos espacios vacíos hay a la derecha de la X
                    if tablero[i][j] == 0:
                        derecha = derecha + 1
                    else:
                        break
                Listaequis[2] = derecha        #Guarda la informacion en la listaequis
                
                izquierda = 0
                for j in range(x - 1, -1, -1):  # Revisa cuantos espacios vacíos hay a la izquierda de la X
                    if tablero[i][j] == 0:
                        izquierda = izquierda + 1
                    else:
                        break
                Listaequis[3] = izquierda         #Guarda la informacion en la listaequis
                
                abajo = 0  # Revisa cuantos espacios vacios hay abajo de la X
                for j in range(i + 1, len(tablero)):
                    if tablero[j][x] == 0:
                        abajo = abajo + 1
                    else:
                        break
                Listaequis[4] = abajo           #Guarda la informacion en la listaequis
                
                arriba = 0  # Revisar espacios arriba
                for j in range(i - 1, -1, -1):  # Se resta porque mientras más arriba en el tablero menor es el número de la fila
                    if tablero[j][x] == 0:
                        arriba = arriba + 1
                    else:
                        break
                Listaequis[5] = arriba           #Guarda la informacion en la listaequis
                
                diagonal45derecha = 0  # busca espacios libres en la diagonal arriba a la derecha 
                for j in range(1, len(tablero)):
                    if i - j < 0 or x + j >= len(tablero[i]):  # evita que recorra fuera del tablero
                        break
                    if tablero[i - j][x + j] == 0:  # Se resta j a i ya que mientras más se sube en el tablero menor es la fila, y se suma j a x ya que para avanzar hacia la derecha x debe crecer
                        diagonal45derecha = diagonal45derecha + 1
                    else:
                        break
                Listaequis[6] = diagonal45derecha      #Guarda la informacion en la listaequis
                
                diagonal45izquierda = 0  # diagonal Izquierda arriba 
                for j in range(1, len(tablero)):
                    if i - j < 0 or x - j < 0:
                        break
                    if tablero[i - j][x - j] == 0:
                        diagonal45izquierda = diagonal45izquierda + 1
                    else:
                        break
                Listaequis[7] = diagonal45izquierda #Guarda la informacion en la listaequis
                
                diagonal135derecha = 0  # Diagonal abajo derecha
                for j in range(1, len(tablero)):
                    if i + j >= len(tablero) or x + j >= len(tablero[i]):
                        break
                    if tablero[i + j][x + j] == 0: 
                        diagonal135derecha = diagonal135derecha + 1
                    else:
                        break
                Listaequis[8] = diagonal135derecha         #Guarda la informacion en la listaequis

                diagonal135izquierda = 0  # Diagonal abajo izquierda
                for j in range(1, len(tablero)):
                    if i + j >= len(tablero) or x - j < 0:
                        break
                    if tablero[i + j][x - j] == 0:
                        diagonal135izquierda = diagonal135izquierda + 1
                    else:
                        break
                Listaequis[9] = diagonal135izquierda        #Guarda la informacion en la listaequis
                
                lista.append(Listaequis)
    
    espacioequis = 0
    cordenadaX = 0
    cordenadaY = 0

    for s in range(len(lista)):
        for a in range(2, 10):
            if lista[s][a] > espacioequis:
                espacioequis = lista[s][a]
                if a == 2:  # analiza la derecha de la X
                    cordenadaY = lista[s][0]
                    if 0 <= lista[s][1] + 1 < len(tablero[0]):
                        cordenadaX = lista[s][1] + 1
                elif a == 3:  # analiza la izquierda de la X
                    cordenadaY = lista[s][0]
                    if 0 <= lista[s][1] - 1 < len(tablero[0]):
                        cordenadaX = lista[s][1] - 1
                elif a == 4:  # analiza abajo de la X
                    if 0 <= lista[s][0] + 1 < len(tablero):
                        cordenadaY = lista[s][0] + 1
                    cordenadaX = lista[s][1]
                elif a == 5:  # analiza arriba de la X
                    if 0 <= lista[s][0] - 1 < len(tablero):
                        cordenadaY = lista[s][0] - 1
                    cordenadaX = lista[s][1]
                elif a == 6:  #analiza  45 grados a la derecha de la X
                    if 0 <= lista[s][0] - 1 < len(tablero):
                        cordenadaY = lista[s][0] - 1
                    if 0 <= lista[s][1] + 1 < len(tablero[0]):
                        cordenadaX = lista[s][1] + 1
                elif a == 7:  # analiza 45 grados a la  izquierda de la X
                    if 0 <= lista[s][0] - 1 < len(tablero):
                        cordenadaY = lista[s][0] - 1
                    if 0 <= lista[s][1] - 1 < len(tablero[0]):
                        cordenadaX = lista[s][1] - 1
                elif a == 8:  # analiza  135 grados a la izquierda de la X
                    if 0 <= lista[s][0] + 1 < len(tablero):
                        cordenadaY = lista[s][0] + 1
                    if 0 <= lista[s][1] - 1 < len(tablero[0]):
                        cordenadaX = lista[s][1] - 1
                elif a == 9:  # analiza 135 grados a la  derecha de la X
                    if 0 <= lista[s][0] + 1 < len(tablero):
                        cordenadaY = lista[s][0] + 1
                    if 0 <= lista[s][1] + 1 < len(tablero[0]):
                        cordenadaX = lista[s][1] + 1
    
    if int(tablero[cordenadaY][cordenadaX])== 0:  #Si el espacio esta vacio lo tomara
            return cordenadaY , cordenadaX

#listaespacios que proviene de la funcion buscador_equis
def capturar(tablero):
    listaespacios = []
    for i in range(len(tablero)):        # i: Recorre números del tablero 
        for x in range(len(tablero)):  # x: Recorre letras del tablero
            if tablero[i][x] == 1:        #almacenara informacion de fichas blancas
                Listaequis = [0,0,0,0,0,0,0,0,0,0]         #esos ceros vacios luego se rellenan con cada dato [[Coordenada y][Coordenada x][Espacios disponibles a su derecha][ Espacios disponibles a su izquierda][ Espacios disponibles a abajo][ Espacios disponibles a  arriba][ Espacios disponibles a 45 grados, sentido derecha][ Espacios disponibles a 45 grados , sentido izquierda][ Espacios disponibles a 135 grados, sentido izquierda][ Espacios disponibles a 135 grados, sentido derecha]]
                Listaequis[0] = i          #dejar guardada en la listaespacios la posición de la X
                Listaequis[1] = x    
                derecha = 0                          #cuenta los ceros

                for j in range(x + 1, len(tablero)):   #Revisa cuantos espacios vacíos hay a la derecha de la X
                    if tablero[i][j] == 2 :          #se pone x + 1 y no solamente x, porque tablero[x][j] es distinto de 0
                        derecha = derecha + 1
                    else:
                        break
                Listaequis[2] = derecha
                izquierda = 0                                     


                for j in range(x - 1, 0, -1):                          #Revisa cuantos espacios vacíos hay a la izquierda de la X
                    if tablero[i][j] == 0:
                        izquierda = izquierda + 1
                    else:
                        break
                Listaequis[3] = izquierda
            
                abajo = 0                                         #Revisa cuantos espacios vacios hay abajo de la X
                for j in range(i + 1, len(tablero)):
                    if tablero[j][x] == 0:
                        abajo = abajo + 1
                    else:
                        break
                Listaequis[4] = abajo
                
                arriba = 0                                       #Revisar espacios arriba
                for j in range(i - 1, 0, -1):                #se resta porque mientras mas arriba en el tablero menor es el número de la fila
                    if tablero[j][x] == 0:
                        arriba = arriba + 1
                    else:
                        break
                Listaequis[5] = arriba
                
                diagonal45derecha = 0                                  #busca espacios libres en la diagonal arriba a la derecha 
                for j in range(1, len(tablero)):
                    if i - j >= len(tablero) or x + j >= len(tablero) or i - j <= 0 or x + j <= 0: #evita que recorra fuera del tablero
                        break
                    if tablero[i - j][x + j] == 0:                #Se resta j a i ya que mientras más se sube en el teblero menor es la fila, y se suma j a x ya que para avanzar hacia la derecha x debe crecer
                        diagonal45derecha = diagonal45derecha + 1  # i: Recorre números del tablero 
                    else:          # x: Recorre letras del tablero
                        break
                Listaequis[6] = diagonal45derecha
                
                diagonal45izquierda = 0              #diagonal Izquierda arriba 
                for j in range(1, len(tablero)):
                    if i - j >= len(tablero) or i - j >= len(tablero) or i - j <= 0 or x - j <= 0:                           # limita a que no se salga del tablero
                        break
                    if tablero[i - j][x - j] == 0:
                        diagonal45izquierda = diagonal45izquierda + 1
                    else:
                        break
                Listaequis[7] = diagonal45izquierda
                
                diagonal135derecha = 0                               #Diagonal abajo derecha
                for j in range(1, len(tablero)):
                    if i + j >= len(tablero) or x + j >= len(tablero):                                  # limita a que no se salga del tablero
                        break
                    if tablero[i + j][x + j] == 0:
                        diagonal135derecha = diagonal135derecha + 1 
                    else:
                        break
                Listaequis[8] = diagonal135derecha

                diagnoal135izquierda = 0                         #Diagonal abajo izquierda
                for j in range(1, len(tablero)):                # limita a que no se salga del tablero
                    if i + j >= len(tablero) or x - j <= 0:
                        break
                    if tablero[i + j][x - j] == 0:
                        diagnoal135izquierda = diagnoal135izquierda + 1
                    else:
                        break
                Listaequis[9] = diagnoal135izquierda
                listaespacios.append(Listaequis)
    cordenadaX = 0
    cordenadaY = 0
    n = len(tablero)
    for s in range(len(listaespacios)):                         #Si no tiene espacio disponible al rededor de la ficha blanca , analizara si tiene la posibilidad de capturar en un rango de una casilla
        for a in range(2, 10):
            if listaespacios[s][a] == 0:
                # Captura a la derecha
                if int(listaespacios[s][1]) + 2 < n:
                    if (tablero[int(listaespacios[s][0])][int(listaespacios[s][1]) + 1] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1]) + 2] == 0):
                        cordenadaY = int(listaespacios[s][0])
                        cordenadaX = int(listaespacios[s][1]) + 2
                
                # Captura a la izquierda
                if int(listaespacios[s][1]) - 2 >= 0:
                    if (tablero[int(listaespacios[s][0])][int(listaespacios[s][1]) - 1] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1]) - 2] == 0):
                        cordenadaY = int(listaespacios[s][0])
                        cordenadaX = int(listaespacios[s][1]) - 2
                
                # Captura abajo
                if int(listaespacios[s][0]) + 2 < n:
                    if (tablero[int(listaespacios[s][0]) + 1][int(listaespacios[s][1])] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0]) + 2][int(listaespacios[s][1])] == 0):
                        cordenadaY = int(listaespacios[s][0]) + 2
                        cordenadaX = int(listaespacios[s][1])
                
                # Captura arriba
                if int(listaespacios[s][0]) - 2 >= 0:
                    if (tablero[int(listaespacios[s][0]) - 1][int(listaespacios[s][1])] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0]) - 2][int(listaespacios[s][1])] == 0):
                        cordenadaY = int(listaespacios[s][0]) - 2
                        cordenadaX = int(listaespacios[s][1])
                
                # Captura diagonal 45 derecha
                if int(listaespacios[s][0]) + 2 < n and int(listaespacios[s][1]) + 2 < n:
                    if (tablero[int(listaespacios[s][0]) + 1][int(listaespacios[s][1]) + 1] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0]) + 2][int(listaespacios[s][1]) + 2] == 0):
                        cordenadaY = int(listaespacios[s][0]) + 2
                        cordenadaX = int(listaespacios[s][1]) + 2
                
                # Captura diagonal 45 izquierda
                if int(listaespacios[s][0]) - 2 >= 0 and int(listaespacios[s][1]) - 2 >= 0:
                    if (tablero[int(listaespacios[s][0]) - 1][int(listaespacios[s][1]) - 1] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0]) - 2][int(listaespacios[s][1]) - 2] == 0):
                        cordenadaY = int(listaespacios[s][0]) - 2
                        cordenadaX = int(listaespacios[s][1]) - 2
                
                # Captura diagonal 135 izquierda
                if int(listaespacios[s][0]) + 2 < n and int(listaespacios[s][1]) - 2 >= 0:
                    if (tablero[int(listaespacios[s][0]) + 1][int(listaespacios[s][1]) - 1] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0]) + 2][int(listaespacios[s][1]) - 2] == 0):
                        cordenadaY = int(listaespacios[s][0]) + 2
                        cordenadaX = int(listaespacios[s][1]) - 2
                
                # Captura diagonal 135 derecha
                if int(listaespacios[s][0]) - 2 >= 0 and int(listaespacios[s][1]) + 2 < n:
                    if (tablero[int(listaespacios[s][0]) - 1][int(listaespacios[s][1]) + 1] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0]) - 2][int(listaespacios[s][1]) + 2] == 0):
                        cordenadaY = int(listaespacios[s][0]) - 2
                        cordenadaX = int(listaespacios[s][1]) + 2
                                                #Si no tiene espacio disponible al rededor de la ficha blanca , analizara si tiene la posibilidad de capturar en un rango de dos casillas
                # Captura dos piezas - derecha
                if int(listaespacios[s][1]) + 3 < n:
                    if (tablero[int(listaespacios[s][0])][int(listaespacios[s][1]) + 1] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1]) + 2] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1]) + 3] == 0):
                        cordenadaY = int(listaespacios[s][0])
                        cordenadaX = int(listaespacios[s][1]) + 3
                
                # Captura dos piezas - izquierda
                if int(listaespacios[s][1]) - 3 >= 0:
                    if (tablero[int(listaespacios[s][0])][int(listaespacios[s][1]) - 1] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1]) - 2] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1]) - 3] == 0):
                        cordenadaY = int(listaespacios[s][0])
                        cordenadaX = int(listaespacios[s][1]) - 3
                
                # Captura dos piezas - abajo
                if int(listaespacios[s][0]) + 3 < n:
                    if (tablero[int(listaespacios[s][0]) + 1][int(listaespacios[s][1])] == -1 and tablero[int(listaespacios[s][0]) + 2][int(listaespacios[s][1])] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0]) + 3][int(listaespacios[s][1])] == 0):
                        cordenadaY = int(listaespacios[s][0]) + 3
                        cordenadaX = int(listaespacios[s][1])
                
                # Captura dos piezas - arriba
                if int(listaespacios[s][0]) - 3 >= 0:
                    if (tablero[int(listaespacios[s][0]) - 1][int(listaespacios[s][1])] == -1 and tablero[int(listaespacios[s][0]) - 2][int(listaespacios[s][1])] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0]) - 3][int(listaespacios[s][1])] == 0):
                        cordenadaY = int(listaespacios[s][0]) - 3
                        cordenadaX = int(listaespacios[s][1])
                
                # Captura dos piezas - diagonal 45 derecha
                if int(listaespacios[s][0]) + 3 < n and int(listaespacios[s][1]) + 3 < n:
                    if (tablero[int(listaespacios[s][0]) + 1][int(listaespacios[s][1]) + 1] == -1 and tablero[int(listaespacios[s][0]) + 2][int(listaespacios[s][1]) + 2] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0]) + 3][int(listaespacios[s][1]) + 3] == 0):
                        cordenadaY = int(listaespacios[s][0]) + 3
                        cordenadaX = int(listaespacios[s][1]) + 3
                
                # Captura dos piezas - diagonal 45 izquierda
                if int(listaespacios[s][0]) - 3 >= 0 and int(listaespacios[s][1]) + 3 < n:
                    if (tablero[int(listaespacios[s][0]) - 1][int(listaespacios[s][1]) + 1] == -1 and tablero[int(listaespacios[s][0]) - 2][int(listaespacios[s][1]) + 2] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0]) - 3][int(listaespacios[s][1]) + 3] == 0):
                        cordenadaY = int(listaespacios[s][0]) - 3
                        cordenadaX = int(listaespacios[s][1]) + 3
                
                # Captura dos piezas - diagonal 135 izquierda
                if int(listaespacios[s][0]) + 3 < n and int(listaespacios[s][1]) - 3 >= 0:
                    if (tablero[int(listaespacios[s][0]) + 1][int(listaespacios[s][1]) - 1] == -1 and tablero[int(listaespacios[s][0]) + 2][int(listaespacios[s][1]) - 2] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0]) + 3][int(listaespacios[s][1]) - 3] == 0):
                        cordenadaY = int(listaespacios[s][0]) + 3
                        cordenadaX = int(listaespacios[s][1]) - 3
                
                # Captura dos piezas - diagonal 135 derecha
                if int(listaespacios[s][0]) - 3 >= 0 and int(listaespacios[s][1]) - 3 >= 0:
                    if (tablero[int(listaespacios[s][0]) - 1][int(listaespacios[s][1]) - 1] == -1 and tablero[int(listaespacios[s][0]) - 2][int(listaespacios[s][1]) - 2] == -1 and tablero[int(listaespacios[s][0])][int(listaespacios[s][1])] == 1 and tablero[int(listaespacios[s][0]) - 3][int(listaespacios[s][1]) - 3] == 0):
                        cordenadaY = int(listaespacios[s][0]) - 3
                        cordenadaX = int(listaespacios[s][1]) - 3             
                
    if int(tablero[cordenadaY][cordenadaX])== 0:
            return cordenadaY , cordenadaX

def rellenar(tablero):
    listaespacios = []
    for i in range(len(tablero)):        # i: Recorre números del tablero 
        for x in range(len(tablero)):  # x: Recorre letras del tablero
            if tablero[i][x] == 1:       #La lista almacenara fichas blancas
                Listaequis = [0,0,0,0,0,0,0,0,0,0]         #esos ceros vacios luego se rellenan con cada dato  [[Coordenada y][Coordenada x][Espacios disponibles a su derecha][ Espacios disponibles a su izquierda][ Espacios disponibles a abajo][ Espacios disponibles a  arriba][ Espacios disponibles a 45 grados, sentido derecha][ Espacios disponibles a 45 grados , sentido izquierda][ Espacios disponibles a 135 grados, sentido izquierda][ Espacios disponibles a 135 grados, sentido derecha]]
                Listaequis[0] = i          #dejar guardada en la listaespacios la posición de la X
                Listaequis[1] = x    
                derecha = 0                          #cuenta los ceros

                for j in range(x + 1, len(tablero)):   #Revisa cuantos espacios vacíos hay a la derecha de la X
                    if tablero[i][j] == 2 :          #se pone x + 1 y no solamente x, porque tablero[x][j] es distinto de 0
                        derecha = derecha + 1
                    else:
                        break
                Listaequis[2] = derecha
                izquierda = 0                                     


                for j in range(x - 1, 0, -1):                          #Revisa cuantos espacios vacíos hay a la izquierda de la X
                    if tablero[i][j] == 0:
                        izquierda = izquierda + 1
                    else:
                        break
                Listaequis[3] = izquierda
            
                abajo = 0                                         #Revisa cuantos espacios vacios hay abajo de la X
                for j in range(i + 1, len(tablero)):
                    if tablero[j][x] == 0:
                        abajo = abajo + 1
                    else:
                        break
                Listaequis[4] = abajo
                
                arriba = 0                                       #Revisar espacios arriba
                for j in range(i - 1, 0, -1):                #se resta porque mientras mas arriba en el tablero menor es el número de la fila
                    if tablero[j][x] == 0:
                        arriba = arriba + 1
                    else:
                        break
                Listaequis[5] = arriba
                
                diagonal45derecha = 0                                  #busca espacios libres en la diagonal arriba a la derecha 
                for j in range(1, len(tablero)):
                    if i - j >= len(tablero) or x + j >= len(tablero) or i - j <= 0 or x + j <= 0: #evita que recorra fuera del tablero
                        break
                    if tablero[i - j][x + j] == 0:                #Se resta j a i ya que mientras más se sube en el teblero menor es la fila, y se suma j a x ya que para avanzar hacia la derecha x debe crecer
                        diagonal45derecha = diagonal45derecha + 1  # i: Recorre números del tablero 
                    else:          # x: Recorre letras del tablero
                        break
                Listaequis[6] = diagonal45derecha
                
                diagonal45izquierda = 0              #diagonal Izquierda arriba 
                for j in range(1, len(tablero)):
                    if i - j >= len(tablero) or i - j >= len(tablero) or i - j <= 0 or x - j <= 0:                           #no se salga del tablero
                        break
                    if tablero[i - j][x - j] == 0:
                        diagonal45izquierda = diagonal45izquierda + 1
                    else:
                        break
                Listaequis[7] = diagonal45izquierda
                
                diagonal135derecha = 0                               #Diagonal abajo derecha
                for j in range(1, len(tablero)):
                    if i + j >= len(tablero) or x + j >= len(tablero):
                        break
                    if tablero[i + j][x + j] == 0:
                        diagonal135derecha = diagonal135derecha + 1
                    else:
                        break
                Listaequis[8] = diagonal135derecha

                diagnoal135izquierda = 0                         #Diagonal abajo izquierda
                for j in range(1, len(tablero)):
                    if i + j >= len(tablero) or x - j <= 0:
                        break
                    if tablero[i + j][x - j] == 0:
                        diagnoal135izquierda = diagnoal135izquierda + 1
                    else:
                        break
                Listaequis[9] = diagnoal135izquierda
                listaespacios.append(Listaequis)
    
    espacios=0
    cordenadaX= 0
    cordenadaY = 0
    for s in range(len(listaespacios)):
        for a in range(2, 10):
            if int(listaespacios[s][a]) > espacios:        # busca  el espacio mayor y lo compara con el anterior en caso de ser mayor guarda las cordenadas del jugador  y lo pondra al lado de la ficha blanca
                if a == 2:  # derecha
                    cordenadaY = listaespacios[s][0]
                    if -1< cordenadaX == int(listaespacios[s][1]) + 1 > 8:
                        cordenadaX = int(listaespacios[s][1]) + 1
                elif a == 3:  # izquierda
                    cordenadaY = listaespacios[s][0]
                    if -1< cordenadaX == int(listaespacios[s][1]) - 1 >8:
                        cordenadaX = int(listaespacios[s][1]) - 1
                elif a == 4:  # abajo
                    if -1< cordenadaY == int(listaespacios[s][0]) + 1>8:
                        cordenadaY = int(listaespacios[s][0]) + 1
                    cordenadaX = int(listaespacios[s][1])
                elif a == 5:  # arriba
                    if -1< cordenadaY == int(listaespacios[s][0]) - 1>8:
                        cordenadaY = int(listaespacios[s][0]) - 1
                    cordenadaX = int(listaespacios[s][1])
                elif a == 6:  # 45 derecha
                    if -1< cordenadaY == int(listaespacios[s][0]) + 1>8:
                        cordenadaY == int(listaespacios[s][0])+ 1
                    if -1< cordenadaX == int(listaespacios[s][1]) + 1>8:
                        cordenadaX = int(listaespacios[s][1]) + 1
                elif a == 7:  # 45 izquierda
                    if -1< cordenadaY == int(listaespacios[s][0]) - 1>8:
                        cordenadaY = int(listaespacios[s][0]) - 1
                    if -1< cordenadaX == int(listaespacios[s][1]) - 1>8:
                        cordenadaX = int(listaespacios[s][1]) - 1
                elif a == 8:  # 135 izquierda
                    if -1< cordenadaY == int(listaespacios[s][0]) + 1>8:
                        cordenadaY = int(listaespacios[s][0]) + 1
                    if -1< cordenadaX == int(listaespacios[s][1]) - 1>8:
                        cordenadaX = int(listaespacios[s][1]) - 1
                elif a == 9:  # 135 derecha
                    if -1< cordenadaY == int(listaespacios[s][0]) - 1>8:
                        cordenadaY = int(listaespacios[s][0]) - 1
                    if -1< cordenadaX == int(listaespacios[s][1]) + 1>8:
                        cordenadaX = int(listaespacios[s][1]) + 1
    if int(tablero[cordenadaY][cordenadaX])== 0:     #analiza si la celda esta vacia de ser asi lo tomara
            return cordenadaY , cordenadaX
                         
def jugada_jugador(tablero):
    #Le define variables a las funciones escritas anteriormente
    jugadas_validas = obtener_jugadas_validas(tablero)
    jugadas_esquinas = marcar_esquinas(tablero)
    jugadas_bordes = rellenar_bordes(tablero)
    jugadas_equis = Alrededor_de_Equis(tablero)
    jugadas_capturar = capturar(tablero)
    jugadas_rellenar = rellenar(tablero)
    
    #ejecuta las funciones explicadas anteriormente de no ser posible, pasara a la siguiente estrategia
    
    while jugadas_esquinas:     
        return jugadas_esquinas

    while jugadas_bordes:
        return jugadas_bordes

    while jugadas_capturar:
        return jugadas_capturar
    while  jugadas_equis:
        return jugadas_equis
    while jugadas_rellenar:
        return jugadas_rellenar       
    while jugadas_validas:
        return random.choice(jugadas_validas)
        
    return None, None

# Cálculo de puntajes para el CPU y el jugador (contar el total de fichas de cada uno)
def obtener_resultado(tablero):
    jugador = -CPU
    puntos_cpu = 0
    puntos_jugador = 0
    for fila in tablero:
        puntos_cpu += fila.count(CPU)
        puntos_jugador += fila.count(jugador)

    return puntos_cpu, puntos_jugador

# Guardar resultados en un archivo CSV
def guardar_resultados(resultados, nombre_archivo="resultados.csv"):
    with open(nombre_archivo, mode='w') as archivo:
        archivo.write("Game,Score CPU,Score Jugador,Parte CPU\n")
        for i, resultado in enumerate(resultados):
            archivo.write(f"{i + 1},{resultado[0]},{resultado[1]},{resultado[2]}\n")

# Función para jugar una ronda
def jugar():
    tablero = inicializar_tablero()
    jugador_actual = random.choice([BLANCO, NEGRO])
    parte_cpu = jugador_actual == CPU
    while True:
        cerrar()         #otorga la opcion de cerrar durante la ejecucion del programa
        mostrar_tablero(ventana, tablero)
        cerrar()            #otorga la opcion de cerrar durante la ejecucion del programa
        jugadas_validas = obtener_jugadas_validas(tablero)
        if not jugadas_validas:
            break
        if jugador_actual == CPU:
            fila, columna = jugada_cpu(tablero)
            cerrar()                #otorga la opcion de cerrar durante la ejecucion del programa
            time.sleep(0)         #le da un retraso a las jugadas para que no sean tan rapidas a la vista
        else:
            fila, columna = jugada_jugador(tablero)
            cerrar()                #otorga la opcion de cerrar durante la ejecucion del programa
            time.sleep(0)         #le da un retraso a las jugadas para que no sean tan rapidas a la vista

        realizar_jugada(tablero, fila, columna, jugador_actual)
        cerrar()                #otorga la opcion de cerrar durante la ejecucion del programa
        jugador_actual = -jugador_actual
    puntos_cpu, puntos_jugador = obtener_resultado(tablero)
    cerrar()
    contador_Cpu=0
    contador_empate=0
    contador_de_victorias_jugador=0
    if MOSTRAR_TERMINAL:
        print(f"Puntos Jugador: {puntos_jugador}")
        print(f"Puntos CPU: {puntos_cpu}")
        print(f"Primer Turno: {'CPU' if parte_cpu else 'Jugador'}")
        if puntos_jugador > puntos_cpu:
            print("Felicitaciones Jugador Gana!")
            contador_de_victorias_jugador = contador_de_victorias_jugador + 1
        elif puntos_jugador < puntos_cpu:
            contador_Cpu = contador_Cpu+1
            print("CPU Gana!")
        else:
            print("Es un empate!")
            contador_empate= contador_empate+1
    
    return puntos_cpu, puntos_jugador, parte_cpu , contador_de_victorias_jugador, contador_empate,contador_Cpu


resultados = []
cpuTotal=0
Victorias_total=0
EmpateTotal=0
for _ in range(RONDAS):
    print("------------- RONDA: " + str(_ + 1)+"---------")
    juego=puntos_cpu, puntos_jugador, parte_cpu , contador_de_victorias_jugador,contador_empate,contador_Cpu= jugar()
    EmpateTotal= EmpateTotal+ contador_empate 
    cpuTotal=  cpuTotal + contador_Cpu
    Victorias_total= Victorias_total + contador_de_victorias_jugador 
    resultados.append(juego)
    cerrar()        #otorga la opcion de cerrar durante la ejecucion del programa
guardar_resultados(resultados)
print("El jugador a ganado un "+ str(int(Victorias_total)*100/RONDAS)+"%")
print("El CPU a ganado un "+ str(int(cpuTotal)*100/RONDAS)+"%")
print("Existe un Empate de un "+ str(int(EmpateTotal)*100/RONDAS)+"%")
input("Presiona cualquier tecla en la terminal para cerrar")
cerrar()            #otorga la opcion de cerrar durante la ejecucion del programa