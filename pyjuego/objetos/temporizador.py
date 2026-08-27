import pygame
from objetos.box import *

class Temporizador:
    def __init__(self, segundos):
        self.tiempo_restante = segundos
        self.ultimo_tick = pygame.time.get_ticks()
        self.terminado = False

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
        self.block = Box(2, 300, 170, 60, "gray", f"Tiempo: {int(self.tiempo_restante)}")
        if self.tiempo_restante <= 10:
            self.block.color = "red"
        else:
            self.block.color = "gray"
        self.block.draw(screen)

    def reset(self):
        self.tiempo_restante = 20
        self.ultimo_tick = pygame.time.get_ticks()
        self.terminado = False