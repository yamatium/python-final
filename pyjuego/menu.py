import pygame

from .configuracion import *
from .manejo_puntaje.puntuacion import puntuacion
from .bucle_juego.juego import *
from .bucle_juego.pantallas_juego import *
from .diccionarios.boton import *
from .sonidos.manejo_sonido import *
from .ingresar_datos import ingresar_jugadores,ingreso_datos


def ingreso_de_jugadores() -> int | None:
        jugadores = ingresar_jugadores()
        return jugadores

    #rehacer con while, linea 52 el for ni se usa, 
def empezar() -> None:
    jugadores = ingreso_de_jugadores()
    if jugadores:
        pygame.mixer.music.fadeout(500)
        musica_menu(2)
        resultados = []
        while len(resultados) < jugadores:
            nombre_jugador = ingreso_datos()
            resultado_jugador = jugar(nombre_jugador)
            resultados.append(resultado_jugador)
        if jugadores > 1:
            mostrar_torneo(resultados)
        musica_menu(1)

def definir_icono_nombre_ventana(icono:pygame.surface)->None:
    #configura el icono y el nombre de la ventana del juego
    pygame.display.set_icon(icono)
    pygame.display.set_caption("FINAL")

def elegir_imagen_gato(numero:int)-> pygame.Surface:
    #crea y configura la imagen 
    img_elejida = pygame.image.load(f"pyjuego/imagenes/gatos/{numero}.png").convert_alpha()
    imagen_escalada = pygame.transform.scale(img_elejida, (400, 400))
    return imagen_escalada

def manejar_teclado(evento:pygame.event.Event)-> bool:
    #manejo de eventos del teclado
    running = True
    print(type(evento))
    if evento.key == pygame.K_m:
        manejar_musica()
    elif evento.key == pygame.K_ESCAPE:
        running = False
    return running


def iniciar()-> None:
    #configuracion inicial
    pygame.init()
    pantalla = crear_superficie_pantalla()
    fuente_final = crear_fuente(150)
    clock = pygame.time.Clock()
    icono = pygame.image.load("pyjuego/imagenes/fred.png")
    definir_icono_nombre_ventana(icono)

    gato = elejir_numero(1,10)
    imagen_gato = elegir_imagen_gato(gato)
    #imagenes
    fondo = pygame.image.load("pyjuego/imagenes/cloud.jpg").convert()
    fondo_escalado = pygame.transform.scale(fondo, (1380, 920)) # WINDOW_HEIGHT= 720,WINDOW_WIDTH=1280

    #objetos a usar
    titulo = fuente_final.render("FINAL", True, "green")

    boton_jugar = crear_boton(40,360,220,100,"white", "Jugar") 
    boton_puntuacion = crear_boton(40,480,220,100, "white", "puntajes")
    boton_musica = crear_boton(1100, 620, 150,70, None, "musica")  # none lo convierte en transparente
    boton_salir = crear_boton(40,600,220,100,"white","Salir")
    botones = [boton_jugar,boton_puntuacion,boton_musica, boton_salir]

    #poner manejo de evento afuera, aca esta anidada
    #las colisiones no tienen acceso a los botones si esta afuera de la funcion
    def manejar_click (pos:tuple)-> bool:
        running = True
        if colision(boton_musica,pos):
            entrar_sonido()
            manejar_musica()
        elif colision(boton_puntuacion, pos):
            entrar_sonido()
            puntuacion()
        elif colision(boton_salir,pos):
            salir_sonido()
            running = False
        elif colision(boton_jugar, pos):
            entrar_sonido()
            empezar()
        return running

    musica_menu(1)
    running = True
    while running:
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = manejar_teclado(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                running = manejar_click(event.pos)
            
        mx, my = pygame.mouse.get_pos()
        pantalla.blit(fondo_escalado, (-50,-100))
        pantalla.blit(titulo, (30,50))
        pantalla.blit(imagen_gato, (800, 100))
        
        dibujar_botones(botones,pantalla, (mx, my))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()




