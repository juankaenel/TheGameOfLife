"""
Creado : 1/7/2020
Autor : Juan Kaenel
"""

import pygame
import numpy as np
import time


#Ancho y alto de pantalla
width, height = 300, 300

#Colores de fondo, negro casi oscuro
bg = 25, 25, 25

#colores de las celulas
live_color = (255,255,255)
dead_color = (128,128,128)

#Creamos la pantalla del juego
pygame.init()

#Creamos pantalla
screen = pygame.display.set_mode((height,width))

#Pintamos el fondo con los colores elegidos
screen.fill(bg)

#cantidad de celdas en eje x e y 
nxC, nyC = 50, 50

#ancho y alto de cada celda viene por la division del ancho de pantalla y cantidad de celdas
dimCW = width / nxC  
dimCH = height / nyC

#Estado de las celdas. Si están vivas tiene valor = 1. Si están muertan = 0
gameState = np.zeros((nxC,nyC))


pauseRun = False
running = True

#formas
gameState[5,3] = 1
gameState[5,4] = 1
gameState[5,5] = 1

gameState[21,21] = 1
gameState[21,22] = 1
gameState[21,23] = 1
gameState[21,24] = 1



#Creamos un bucle para mostrar la pantalla
while running: 

    #Dentro de los bucles for estamos aplicando las reglas a cada una de las celdas en forma secuencial. Significa que si cambie la celda anterior, ahora en el calculo de la celda actual estoy teniendo en cuenta los calculos anteriores. Para solucionar esto
            #los cambios deberían producirse al mismo tiempo en cada periodo de tiempo

            #Hacemos en cada iteración una copia del estado actual del juego
            newGameState = np.copy(gameState) # en esta copia guardaremos cada cada una de las actualizaciones que realizamos en cada celda del juego y la que usaremos para dibujar los cuadraditos anteriores que nos hagan falta

            #Registramos los eventos del teclado
            ev = pygame.event.get()

            for event in ev:

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    pauseRun = not pauseRun

                #detecta si se presiona una tecla
                mouseClick = pygame.mouse.get_pressed()
                if sum(mouseClick) > 0:
                    posX, posY = pygame.mouse.get_pos()
                    celX, celY = int(np.floor(posX/dimCW)), int(np.floor(posY/dimCH))
                    newGameState[celX,celY] = not mouseClick[2]
        
            #limpiamos la pantalla con el color elegido de fondo por cada estado así no se van superponiendo las celdas
            screen.fill(bg)
            #time.sleep(0.1)

    #recorremos cada una de las celdas que hemos generado
            for y in range(0, nxC):
                for x in range(0, nyC):
                    
                    if not pauseRun:
                        #Calculamos el número de vecinos. Utilizamos el módulo con el concepto de un toroide. Si tengo 5 posiciones, cuando llegue a la 5ta que vuelva a la primera posición
                        n_neigh = gameState[(x-1) % nxC, (y-1) %  nyC] + \
                                  gameState[(x)   % nxC, (y-1) %  nyC] + \
                                  gameState[(x+1) % nxC, (y-1) %  nyC] + \
                                  gameState[(x-1) % nxC, (y)   %  nyC] + \
                                  gameState[(x+1) % nxC, (y)   %  nyC] + \
                                  gameState[(x-1) % nxC, (y+1) %  nyC] + \
                                  gameState[(x)   % nxC, (y+1) %  nyC] + \
                                  gameState[(x+1) % nxC, (y+1) %  nyC]

                        #Reglas del juego ->  Si están vivas tiene valor = 1. Si están muertan = 0

                        #Regla 1: Una célula muerta con exactamente 3 vecinas vivas, "revive".
                        if gameState[x, y ] == 0 and n_neigh == 3:
                            newGameState[x, y] = 1

                        #Regla 2: Una célula viva con menos de 2 o más de 3 vecinas vivas, "muere". Acabará muriendo por soledad o sobrepoblación
                        elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                                newGameState[x, y] = 0 

                        #Creamos el poligono de cada celda a dibujar
                        poly = [((x)   * dimCH, y     * dimCH),
                                ((x+1) * dimCW, y     * dimCH),
                                ((x+1) * dimCW, (y+1) * dimCH),
                                ((x)   * dimCW, (y+1) * dimCH)]

                        #Dibujamos la celda para cada par de eje x e y
                        #Si está viva haceme la celda de color blanco y sin borde
                        if newGameState[x,y] == 1:
                           pygame.draw.polygon(screen, live_color, poly, 0)
                        
                        #Si está muerta tiene un borde de 1
                        else:
                            pygame.draw.polygon(screen, dead_color, poly ,1)
                     
            #Actualizamos el estado del juego, haciendo que el estado sea el actual
            gameState = np.copy(newGameState)
            
            time.sleep(0.1)
            #Actualizamos la pantalla         
            pygame.display.flip()

pygame.quit()