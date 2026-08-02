import pygame, os
from settings import *
from box import Box
from ingresar_datos import *

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def borrar_puntuacion():
    try:
        os.remove("puntuacion.txt")
    except FileNotFoundError:
        pass  # already deleted, nothing to do

def puntuacion():
    puntajes = cargar_puntuacion()

    block_titulo = Box(450, 50, 400, 60, "green", "Leaderboard")
    block_borrar = Box(450, 650, 400, 60, "black", "Borrar historial")
    block_salir = Box(200, 450, 400, 60, "gray", "salir")
    
    blocks_puntaje = []
    y = 150
    for p in puntajes:
        texto = f"Jugador: {p['nombre']} | estado final: {p['estado']} | puntaje: {p['puntaje']}"
        blocks_puntaje.append(Box(450, y, 600, 60, "gray", texto))
        y += 70

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if block_borrar.collidepoint(event.pos):
                        borrar_puntuacion()
                        blocks_puntaje = []  # clear boxes from screen
                    if block_salir.collidepoint(event.pos):
                        running = False

        screen.fill(COLORS["royalblue"])
        block_titulo.draw(screen)
        block_borrar.draw(screen)
        block_salir.draw(screen)

        for block in blocks_puntaje:
            block.draw(screen)

        pygame.display.flip()
        clock.tick(60)