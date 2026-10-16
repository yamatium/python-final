import pygame

from pyjuego.configuracion import crear_fuente,crear_superficie_pantalla
from pyjuego.diccionarios.boton import * 

pantalla = crear_superficie_pantalla()
fuente = crear_fuente(50)

def dibujar_opciones(screen:pygame.surface,preguntas:dict ,pregunta_aleatoria:int) -> None:
    #dibuja las string de opciones de respuesta a la pregunta
    opciones = preguntas[pregunta_aleatoria]["opciones"]
    posiciones = [(250, 330), (650, 330), (250, 430), (650, 430)]

    for i in range(4):
        fuente_opcion = fuente.render(opciones[i], True, "black")
        x, y = posiciones[i]
        screen.blit(fuente_opcion, (x, y))

def dibujar_estado(nombre:str, estado_final:bool) -> list: # dibuja al final de la partida
    #dibuja los resultados del jugador al terminar la partida
    nombre = fuente.render(f"Jugador: {nombre}", True, "black")
    if estado_final:
        final = fuente.render("Ganaste!", True, "black")
    else:
        final = fuente.render("Perdiste!", True, "black")

    resultado = [nombre ,final]
    return resultado

def dibujar_pregunta(pregunta:list, x:int,y:int) ->None:
    #dibuja la pregunta en la pantalla
    for linea in pregunta:
        linea = fuente.render(linea, True, "black")
        pantalla.blit(linea, (x, y))
        y += 60

def crear_botones_opciones(preguntas:dict,pregunta_aleatoria:int) -> list:
    #dibuja los botones donde van las respuestas
    cantidad = 4
    lista = []
    opciones = preguntas[pregunta_aleatoria]["opciones"]
    posiciones = [(250, 400), (700, 400), (250, 510), (700, 510)]
    ancho = 150
    alto = 100

    for i in range(cantidad):
        x,y = posiciones[i]
        boton = crear_boton(x,y,ancho,alto, None, opciones[i])
        lista.append(boton)
    return lista