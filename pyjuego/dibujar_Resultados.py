import pygame
from box import Box

class dibujar_Resultados:
    def __init__(self, x, y, cell_w=150, cell_h=50, color="white", border_color=(0, 0, 0), border_width=2):
        self.x = x
        self.y = y
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.color = color
        self.border_color = border_color
        self.border_width = border_width

        self.headers = ["Sala", "Puntaje Sala", "Puntaje Total"]
        self.resultados_salas = []  # filas dinamicas
        self.tabla_boxes = []       # grid de Box, se reconstruye cada vez que cambia

        self._reconstruir()

    def agregar_resultado(self, nombre_sala, puntaje_sala, puntaje_total):
        self.resultados_salas.append([
            nombre_sala,
            str(puntaje_sala),
            str(puntaje_total),
        ])
        self._reconstruir()

    def _reconstruir(self):
        data = [self.headers] + self.resultados_salas
        self.tabla_boxes = []
        for row_index, row_data in enumerate(data):
            fila_boxes = []
            for col_index, valor in enumerate(row_data):
                cell_x = self.x + col_index * self.cell_w
                cell_y = self.y + row_index * self.cell_h
                box = Box(cell_x, cell_y, self.cell_w, self.cell_h, self.color, str(valor))
                fila_boxes.append(box)
            self.tabla_boxes.append(fila_boxes)

    def draw(self, surface):
        for fila in self.tabla_boxes:
            for box in fila:
                box.draw(surface)
                pygame.draw.rect(surface, self.border_color, box.rect, self.border_width)

class TablaResultadoFinal:
    def __init__(self, x, y, w=200, h=50, color="white", border_color=(0, 0, 0), border_width=2):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.border_color = border_color
        self.border_width = border_width

        self.estado = ["Nombre", "Estado Final"]
        self.resultados = []
        self.tabla_boxes = []

        self._reconstruir()

    def agregar_resultado(self, nombre, gano):
        estado_texto = "Completo" if gano else "No Completo"
        self.resultados.append([nombre, estado_texto])
        self._reconstruir()

    def _reconstruir(self):
        data = [self.estado] + self.resultados
        self.tabla_boxes = []
        for row_index, row_data in enumerate(data):
            fila_boxes = []
            for col_index, valor in enumerate(row_data):
                cell_x = self.x + col_index * self.w
                cell_y = self.y + row_index * self.h
                box = Box(cell_x, cell_y, self.w, self.h, self.color, str(valor))
                fila_boxes.append(box)
            self.tabla_boxes.append(fila_boxes)

    def draw(self, surface):
        for fila in self.tabla_boxes:
            for box in fila:
                box.draw(surface)
                pygame.draw.rect(surface, self.border_color, box.rect, self.border_width)