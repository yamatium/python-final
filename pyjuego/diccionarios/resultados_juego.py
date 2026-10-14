import pygame

from pyjuego.configuracion import *

def crear_resultados(x:int,y:int,ancho:int,alto:int)-> dict:
    #crea un diccionario de resultados para el jugador
    resultados = {}
    resultados["x"] = x
    resultados["y"] = y
    resultados["ancho"] = ancho
    resultados["alto"] = alto
    resultados["columnas"] = ["sala", "puntaje Sala", "Puntaje Total"]
    resultados["resultados_salas"] = []

    return resultados

def completar_resultados(resultados:dict,numero_sala:int, puntaje_sala:int, puntaje_total:int)-> None:
    #agrega los puntajes de cada sala al diccionario de resultados del jugador
    resultados["resultados_salas"].append([numero_sala, puntaje_sala, puntaje_total])


#combinar fila y columna por dibujar_matriz
def dibujar_fila(resultados:dict, fuente:pygame.font.Font, superficie:pygame.Surface, ancho:int)-> None:
    #dibuja las filas de encabezados
    posicion_x = resultados["x"]
    posicion_y = resultados["y"]
    for encabezado in resultados["columnas"]:
        texto = fuente.render(encabezado, True, "black")
        superficie.blit(texto, (posicion_x, posicion_y))
        posicion_x += ancho

def dibujar_columna(resultados:dict,fuente:pygame.font.Font ,superficie:pygame.Surface,ancho:int,alto:int)-> None:
    #dibuja el contenido de los encabezados
    fila = 1
    for sala in resultados["resultados_salas"]:
        celda_x = resultados["x"]
        celda_y = resultados["y"] + 30 + fila * alto
        for valor in sala:
            #print(valor)
            texto = fuente.render(str(valor), True, "black")
            superficie.blit(texto, (celda_x , celda_y))
            celda_x += ancho
        fila += 1

def dibujar_resultados(resultados: dict,superficie:pygame.Surface)-> None:
    #llama a las funciones de dibujo para la pantalla de resultado del jugador
    fuente = crear_fuente(50)
    ancho = 250
    alto = 50

    dibujar_fila(resultados,fuente,superficie,ancho)
    dibujar_columna(resultados,fuente,superficie,ancho,alto)
