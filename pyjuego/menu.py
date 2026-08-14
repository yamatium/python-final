import pygame, random
from configuracion import *
from objetos.TextInputBox import *
from objetos.box import Box,dibujar_botones
from juego import *
from puntuacion import *

#configuracion inicial
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("wawa")
icon = pygame.image.load("assets/images/fred.png")
pygame.display.set_icon(icon)
font = pygame.font.SysFont(None, 150)

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
a = font.render("FINAL", True, "green")
text_input_box = TextInputBox(650, 150, 400, font)
group = pygame.sprite.Group(text_input_box)
rect_puntuacion = Box(40,480,220,100, "white", "puntajes")
rect_salir = Box(40,600,220,100,"white", "Salir")
rect_jugar = Box(40,360,220,100,"white", "Jugar")
rect_musica = Box(1100, 620, 150,70, "white", "musica")

botones = [rect_jugar, rect_puntuacion, rect_musica, rect_salir]
#variables 
running = True

def empezar():
    jugadores = ingresar_jugadores()
    if not jugadores :
        return # exits to the main menu
    resultados = []
    for i in range(jugadores):
        resultado_jugador = jugar()
        if resultado_jugador is None:
            return # exits to the main menu
        resultados.append(resultado_jugador)
    mostrar_torneo(resultados)

musica_menu()

while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:  #K_SPACE usar para pausar el juego en juego.py pygame.K_SPACE
                manejar_musica()
            if event.key == pygame.K_ESCAPE:
                running = False 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if rect_musica.collidepoint(event.pos):
                    entrar_sonido()
                    manejar_musica()
                if rect_puntuacion.collidepoint(event.pos):
                    rect_puntuacion.sonidoClick()
                    puntuacion()
                if rect_salir.collidepoint(event.pos):
                    rect_salir.sonidoClick("salir")
                    running = False
                if rect_jugar.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(500)
                    entrar_sonido()
                    empezar()
                    pygame.mixer.music.play(-1)
                
           
    mx, my = pygame.mouse.get_pos()
    screen.blit(fondo_escalado, (-50,-100))
    screen.blit(a, (30,50))
    screen.blit(gato_actual, (800, 100))

    dibujar_botones(botones, screen, (mx, my))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()




