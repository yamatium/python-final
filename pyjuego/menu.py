import pygame, random
from configuracion import *
from objetos.TextInputBox import *
from objetos.box import Box
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

gatos = []
for i in range(1,11):
    img = pygame.image.load(f"pyjuego/imagenes/gatos/{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (400, 400))
    gatos.append(img)
gato_actual = random.choice(gatos)



a = font.render("FINAL", True, "green")

#imagenes
fondo = pygame.image.load("pyjuego/imagenes/cloud.jpg").convert()
fondo_escalado = pygame.transform.scale(fondo, (WINDOW_WIDTH + 100, WINDOW_HEIGHT +200 ))

#objetos a usar
text_input_box = TextInputBox(650, 150, 400, font)
group = pygame.sprite.Group(text_input_box)
rect_puntuacion = Box(40,480,220,100, "white", "puntajes")
rect_salir = Box(40,600,220,100,"white", "Salir")
rect_jugar = Box(40,360,220,100,"white", "Jugar")
rect_musica = Box(1100, 620, 150,70, "white", "musica")

botones = [rect_jugar, rect_puntuacion, rect_musica, rect_salir]
#variables 
click = False
pausar_musica = False
running = True

musica_menu()

while running:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:  #K_SPACE usar para pausar el juego en juego.py pygame.K_SPACE
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if event.key == pygame.K_ESCAPE:
                running = False 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
                print("click")
           
    
    mx, my = pygame.mouse.get_pos()
    screen.blit(fondo_escalado, (-50,-100))
    
    
    #block5.draw(screen)
    screen.blit(a, (30,50))
    rect_puntuacion.draw(screen)
    rect_salir.draw(screen)
    rect_jugar.draw(screen)
    rect_musica.draw(screen)
    screen.blit(gato_actual, (800, 100))

    for boton in botones:
        if boton.collidepoint((mx,my)):
            boton.color = COLORS["lightblue"]
        else:
            boton.color = COLORS["white"]

    if rect_musica.collidepoint((mx,my)):
        if click:
            entrar_sonido()
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

    if rect_puntuacion.collidepoint((mx,my)):
        if click:
            entrar_sonido()
            puntuacion()
    if rect_salir.collidepoint((mx,my)):
        if click:
            salir_sonido()
            running = False
    if rect_jugar.collidepoint((mx,my)):
        if click:
            pygame.mixer.music.stop()
            entrar_sonido()
            jugadores = ingresar_jugadores()
            resultados = []
            for i in range(jugadores):
                resultado_jugador = jugar()
                resultados.append(resultado_jugador)
            mostrar_torneo(resultados)
            pygame.mixer.music.play(-1)

    click = False
    pygame.display.flip()
    clock.tick(60)

pygame.quit()




