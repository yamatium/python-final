import pygame

from pyjuego.configuracion import *

def crear_resultados(x:int,y:int,ancho:int,alto:int)-> dict:
    resultados = {}
    resultados["x"] = x
    resultados["y"] = y
    resultados["ancho"] = ancho
    resultados["alto"] = alto
    resultados["columnas"] = ["sala", "puntaje Sala", "Puntaje Total"]
    resultados["resultados_salas"] = []

    return resultados

def completar_resultados(resultados:dict,nombre_sala, puntaje_sala, puntaje_total):
    resultados["resultados_salas"].append([nombre_sala, puntaje_sala, puntaje_total])


#cambiar por una casera
def dibujar_resultados(resultados: dict, superficie):
    fuente = crear_fuente_c(50)
    ancho_columna = 250
    alto_fila = 50

    # draw column headers
    celda_x = resultados["x"]
    for encabezado in resultados["columnas"]:
        texto = fuente.render(str(encabezado), True, "black")
        superficie.blit(texto, (celda_x, resultados["y"]))
        celda_x += ancho_columna

    # draw each row of data
    fila = 1
    for sala in resultados["resultados_salas"]:
        celda_x = resultados["x"]
        celda_y = resultados["y"] + fila * alto_fila
        for valor in sala:
            texto = fuente.render(str(valor), True, "black")
            superficie.blit(texto, (celda_x, celda_y))
            celda_x += ancho_columna
        fila += 1
