import pygame
from objetos.box import Box

class dibujar_Resultados:
    def __init__(self, x, y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.columnas = ["Sala", "Puntaje Sala", "Puntaje Total"]
        self.resultados_salas = []

    def agregar_resultado(self, nombre_sala, puntaje_sala, puntaje_total):
        self.resultados_salas.append([
            nombre_sala,
            str(puntaje_sala),
            str(puntaje_total),])

    def draw(self, surface, font):
        data = [self.columnas] + self.resultados_salas
        ancho_columna = [self.w, self.w + 80, self.w + 80]
        fila = 0
        for columna in data:
            col_index = 0
            cell_x = self.x
            extra = 30 if fila > 0 else 0 # para poner mas abajo por las ventanas del castillo
            cell_y = self.y + fila * self.h + extra
            for valor in columna:
                texto = font.render(str(valor), True, "black")
                surface.blit(texto, (cell_x, cell_y))
                cell_x += ancho_columna[col_index]
                col_index += 1
            fila += 1