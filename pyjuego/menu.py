import pygame, random

from .configuracion import *
from .juego import *
from .puntuacion import *
from .pantallas_juego import *
from .diccionarios.boton import *


def iniciar()-> None:
    #configuracion inicial
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("wawa")
    icono = pygame.image.load("pyjuego/imagenes/fred.png")
    pygame.display.set_icon(icono)

    # imagen de menu
    #elegir numero entre 1 y 11
    #img = pygame.image.load(f"pyjuego/imagenes/gatos/{numero_elejido}.png").convert_alpha()
    #no cargar todos los gatos en una lista, elejir 1 numero con una funcion casera y dibujar la imagen

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

    boton_jugar = crear_boton(40,360,220,100,"white", "Jugar") 
    boton_puntuacion = crear_boton(40,480,220,100, "white", "puntajes")
    boton_musica = crear_boton(1100, 620, 150,70, None, "musica")  # none lo convierte en transparente
    boton_salir = crear_boton(40,600,220,100,"white","Salir")
    botones = [boton_jugar,boton_puntuacion,boton_musica, boton_salir]


    #rehacer con while, linea 52 el for ni se usa, 
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
                break  # cancelado a mitad de partida , sacar , un jugador no puede terminar el torneo saliendo
            resultados.append(resultado_jugador)
        if len(resultados) == jugadores and jugadores > 1:
            mostrar_torneo(resultados)
        musica_menu(1)



    musica_menu(1)
    running = True
    while running:
        event_list = pygame.event.get()
        #hacer manejo de event, 
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
                    if colision(boton_musica,event.pos):
                        entrar_sonido()
                        manejar_musica()
                    if colision(boton_puntuacion, event.pos):
                        entrar_sonido()
                        puntuacion()
                    if colision(boton_salir,event.pos):
                        salir_sonido()
                        running = False
                    if colision(boton_jugar, event.pos):
                        entrar_sonido()
                        empezar()
                    
            
        mx, my = pygame.mouse.get_pos() #ya regresa una tupla
        screen.blit(fondo_escalado, (-50,-100))
        screen.blit(a, (30,50))
        screen.blit(gato_actual, (800, 100))

        dibujar_botonesd(botones,screen, (mx, my))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()




