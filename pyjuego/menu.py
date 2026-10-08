import pygame, random

from .configuracion import *
from .bucle_juego.juego import *
from .puntuacion import *
from .bucle_juego.pantallas_juego import *
from .diccionarios.boton import *


def ingreso_de_jugadores() -> int | None:
        jugadores = ingresar_jugadores()
        return jugadores

    #rehacer con while, linea 52 el for ni se usa, 
def empezar() -> None:
    jugadores = ingreso_de_jugadores()
    if jugadores :
        pygame.mixer.music.fadeout(500)
        musica_menu(2)
        resultados = []
        while len(resultados) < jugadores: 
            resultado_jugador = jugar() # en modo torneo al apretar salir rompe, sacar el boton salir en torneo y que defaultee a resultado 0 y no respondio 1 pregunta
            resultados.append(resultado_jugador)   
        if jugadores > 1:
            mostrar_torneo(resultados)
        musica_menu(1)


def iniciar()-> None:
    #configuracion inicial
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    fuente_final = crear_fuente(150)
    clock = pygame.time.Clock()
    pygame.display.set_caption("wawa")
    icono = pygame.image.load("pyjuego/imagenes/fred.png")
    pygame.display.set_icon(icono)

    #no cargar todos los gatos en una lista, elejir 1 numero con una funcion casera y dibujar la imagen
    gato = elejir_numero(1,10)
    img_elejida = pygame.image.load(f"pyjuego/imagenes/gatos/{gato}.png").convert_alpha()
    imagen_gato = pygame.transform.scale(img_elejida, (400, 400))

    #imagenes
    fondo = pygame.image.load("pyjuego/imagenes/cloud.jpg").convert()
    fondo_escalado = pygame.transform.scale(fondo, (WINDOW_WIDTH + 100, WINDOW_HEIGHT +200 ))

    #objetos a usar
    titulo = fuente_final.render("FINAL", True, "green")

    boton_jugar = crear_boton(40,360,220,100,"white", "Jugar") 
    boton_puntuacion = crear_boton(40,480,220,100, "white", "puntajes")
    boton_musica = crear_boton(1100, 620, 150,70, None, "musica")  # none lo convierte en transparente
    boton_salir = crear_boton(40,600,220,100,"white","Salir")
    botones = [boton_jugar,boton_puntuacion,boton_musica, boton_salir]

    def manejar_click (pos:tuple)-> bool:
        running = True
        if colision(boton_musica,pos):
            entrar_sonido()
            manejar_musica()
        if colision(boton_puntuacion, pos):
            entrar_sonido()
            puntuacion()
        if colision(boton_salir,pos):
            salir_sonido()
            running = False
        if colision(boton_jugar, pos):
            entrar_sonido()
            empezar()
        return running

    def manejar_teclado(event)-> bool:
        running = True
        if event.key == pygame.K_m:
            manejar_musica()
        elif event.key == pygame.K_ESCAPE:
            running = False
        return running


    musica_menu(1)
    running = True
    while running:
        event_list = pygame.event.get()
        #hacer manejo de event, 
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = manejar_teclado(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                running = manejar_click(event.pos)
            
        mx, my = pygame.mouse.get_pos() #ya regresa una tupla
        screen.blit(fondo_escalado, (-50,-100))
        screen.blit(titulo, (30,50))
        screen.blit(imagen_gato, (800, 100))
        

        dibujar_botonesd(botones,screen, (mx, my))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()




