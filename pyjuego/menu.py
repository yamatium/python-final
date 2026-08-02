import pygame
from settings import *
from TextInputBox import *
from box import Box
from juego import *
from puntuacion import *

#configuracion inicial
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("wawa")
icon = pygame.image.load("assets/images/fred.png")
pygame.display.set_icon(icon)
font = pygame.font.SysFont(None, 100)

#objetos a usar
text_input_box = TextInputBox(650, 150, 400, font)
group = pygame.sprite.Group(text_input_box)
block = Box(450,430,200,70, "white", "puntajes")
block2 = Box(450,530,200,70,"white", "Opciones")
block3 = Box(450,630,200,70,"white", "Salir")
block4 = Box(450,330,200,70,"white", "Jugar")
block5 = Box(400,30,450,250,"green", "Titulo")
block_bg = Box((WINDOW_WIDTH / 3)+100,0,610,WINDOW_HEIGHT,"red")



def puntaje():
    blockjuego = Box(450,330,200,70,"white", "Puntaje")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(COLORS["royalblue"])
        blockjuego.draw(screen)
        pygame.display.flip()
        clock.tick(60) 

def opciones():
    blockjuego = Box(450,330,200,70,"white", "Opciones")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(COLORS["royalblue"])
        blockjuego.draw(screen)
        pygame.display.flip()
        clock.tick(60) 

#variables 
click = False
juego_pausa = False
running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.TEXTINPUT:
            print(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                juego_pausa = True
                print("pausa")
            if event.key == pygame.K_ESCAPE:
                running = False 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
                print("click")
           
    
    mx, my = pygame.mouse.get_pos()
    #group.update(event_list)
    screen.fill(COLORS["royalblue"])
    
    #block_bg.draw(screen)
    #group.draw(screen)
    block5.draw(screen)
    block.draw(screen)
    block2.draw(screen)
    block3.draw(screen)
    block4.draw(screen)


    if block.collidepoint((mx,my)):
        if click:
            puntuacion()

    if block2.collidepoint((mx,my)):
        if click:
            opciones()
    if block3.collidepoint((mx,my)):
        if click:
            running = False
    if block4.collidepoint((mx,my)):
        if click:
            jugadores = ingresar_jugadores()
            resultados = []
            for i in range(jugadores):
                resultado_jugador = jugar()
                resultados.append(resultado_jugador)
            mostrar_torneo(resultados)

    click = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()




