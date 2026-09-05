import pygame, random

from configuracion import *
from objetos.TextInputBox import *
from objetos.box import Box,dibujar_botones
from juego import *
from puntuacion import *

#configuracion inicial
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("wawa")
icon = pygame.image.load("assets/images/fred.png")
pygame.display.set_icon(icon)

# imagen de menu
gatos = []
for i in range(1,11):
    img = pygame.image.load(f"pyjuego/imagenes/gatos/{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (400, 400))
    gatos.append(img)
gato_actual = random.choice(gatos)

#imagenes
fondo = pygame.image.load("pyjuego/imagenes/cloud.jpg").convert()
fondo_escalado = pygame.transform.scale(fondo, (WINDOW_WIDTH + 100, WINDOW_HEIGHT +200 ))

#objetos a usar
a = font_final.render("FINAL", True, "green")
boton_puntuacion = Box(40,480,220,100, "white", "puntajes")
boton_salir = Box(40,600,220,100,"white", "Salir")
boton_jugar = Box(40,360,220,100,"white", "Jugar")
boton_musica = Box(1100, 620, 150,70, "white", "musica")
botones = [boton_jugar, boton_puntuacion, boton_musica, boton_salir]


def empezar() -> None:
    jugadores = ingresar_jugadores()
    if not jugadores:
        return  # cancelado al ingresar jugadores, musica del menu no se toca
    pygame.mixer.music.fadeout(500)
    musica_menu(2)
    resultados = []
    for i in range(jugadores):
        resultado_jugador = jugar()
        if resultado_jugador is None:
            break  # cancelado a mitad de partida
        resultados.append(resultado_jugador)
    if len(resultados) == jugadores and jugadores > 1:
        mostrar_torneo(resultados)
    musica_menu(1)



musica_menu(1)
running = True
while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                manejar_musica()
            if event.key == pygame.K_ESCAPE:
                running = False 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if boton_musica.collidepoint(event.pos):
                    entrar_sonido()
                    manejar_musica()
                if boton_puntuacion.collidepoint(event.pos):
                    boton_puntuacion.sonidoClick()
                    puntuacion()
                if boton_salir.collidepoint(event.pos):
                    boton_salir.sonidoClick("salir")
                    running = False
                if boton_jugar.collidepoint(event.pos):
                    entrar_sonido()
                    empezar()
                
           
    mx, my = pygame.mouse.get_pos()
    screen.blit(fondo_escalado, (-50,-100))
    screen.blit(a, (30,50))
    screen.blit(gato_actual, (800, 100))

    dibujar_botones(botones, screen, (mx, my))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()




