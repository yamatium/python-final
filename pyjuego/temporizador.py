import pygame
from box import *


class Temporizador:
    def __init__(self, segundos):
        self.tiempo_restante = segundos
        self.ultimo_tick = pygame.time.get_ticks()
        self.terminado = False
        self.block = Box(300, 150, 200, 70, "gray", f"Tiempo: {segundos}")

    def update(self):
        if not self.terminado:
            ahora = pygame.time.get_ticks()
            elapsed = (ahora - self.ultimo_tick) / 1000
            self.tiempo_restante -= elapsed  
            self.ultimo_tick = ahora

            if self.tiempo_restante <= 0:
                self.tiempo_restante = 0
                self.terminado = True

    def draw(self, screen):
        self.block.texto = f"Tiempo: {int(self.tiempo_restante)}"
        #self.block.color = "red" if self.tiempo_restante <= 10 else "gray"
        self.block.draw(screen)

    def reset(self):
        self.tiempo_restante = 30
        self.ultimo_tick = pygame.time.get_ticks()
        self.terminado = False