import pygame

from pyjuego.configuracion import *

def pygame_traer_tick() -> int:
    tick = pygame.time.get_ticks()
    return tick

def crear_cronometro(tiempo:int)-> dict:
    cronometro = {}
    cronometro["tiempo_restante"] = tiempo
    cronometro["tiempo_terminado"] = False
    cronometro["pygame_tiempo_tick"] = pygame_traer_tick()
    return cronometro


def actualizar_tiempo(cronometro: dict) -> None:
    if not cronometro["tiempo_terminado"]:
        ahora = pygame.time.get_ticks()
        pasado = (ahora - cronometro["pygame_tiempo_tick"]) / 1000
        cronometro["tiempo_restante"] -= pasado
        cronometro["pygame_tiempo_tick"] = ahora
        if cronometro["tiempo_restante"] <= 0:
             cronometro["tiempo_terminado"] = True

#pantalla = class 'pygame.surface.Surface' 
def dibujar_cronometro(cronometro:dict, pantalla) -> None:
     if cronometro["tiempo_restante"] <= 11:
          color_fondo = "red"
     else:
        color_fondo = "gray"
     segundos = int(cronometro["tiempo_restante"])
     rectangulo = font.render(f"Tiempo: {segundos}", True, "black", color_fondo)
     pantalla.blit(rectangulo,(2,300))

def resetear_cronometro(cronometro:dict)-> None:
     cronometro["tiempo_restante"] = 20
     cronometro["pygame_tiempo_tick"] = pygame_traer_tick()
     cronometro["tiempo_terminado"] = False
     

