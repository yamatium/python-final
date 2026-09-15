import pygame

from objetos.Caja import *
from configuracion import *

class Temporizador:
    def __init__(self, segundos):
        self.tiempo_restante = segundos
        self.ultimo_tick = pygame.time.get_ticks()
        self.terminado = False
        self.bandera_pausa = False

    def actualizar(self) -> None:
        if not self.terminado:
            ahora = pygame.time.get_ticks()
            pasado = (ahora - self.ultimo_tick) / 1000
            self.tiempo_restante -= pasado 
            self.ultimo_tick = ahora
            if self.tiempo_restante <= 0:
                self.terminado = True

    def dibujar(self, screen) -> None:
        if self.tiempo_restante <= 11:
            color_fondo = "red"
        else:
            color_fondo = "gray"
        caja = font.render(f"Tiempo: {int(self.tiempo_restante)}", True, "black",color_fondo)
        screen.blit(caja, (2,300))
        
    def resetear(self)-> None:
        self.tiempo_restante = 20
        self.ultimo_tick = pygame.time.get_ticks()
        self.terminado = False