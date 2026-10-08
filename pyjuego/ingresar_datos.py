import pygame
from .configuracion import *
from .diccionarios.boton import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
#font = pygame.font.SysFont(None, 50)
fuente = crear_fuente(50)


def validar_ascii_letra(caracter)-> bool:
    #valida que el rango sea de la a a la z 
    valor_ascii_minimo = 97
    valor_ascii_maximo = 122

    return valor_ascii_minimo <= ord(caracter) <= valor_ascii_maximo #revisar si se puede regresar asi,(programacion 2) sino cambiar con un if return o while

def validar_ascii_numero(caracter)-> bool:
    #valida que el rango sea del 1 al 9 
    valor_ascii_minimo = 48
    valor_ascii_maximo = 57

    return valor_ascii_minimo <= ord(caracter) <= valor_ascii_maximo #revisar si se puede regresar asi,(programacion 2) sino cambiar con un if return

def validar_letra(caracter) ->bool:
    resultado = ""
    if len(caracter) == 1 and validar_ascii_letra(caracter):
      resultado = caracter
    
    return resultado

 

def validar_numero(caracter: str)-> str:
    # poner validador de len caracter == 1
    #len(caracter) ==1 evita que flechas o no letras crasheen
    resultado = ""
    if len(caracter) == 1 and validar_ascii_numero(caracter):
        resultado = caracter

    return resultado
    


def ingreso_datos():
    fondo = pygame.image.load("pyjuego/imagenes/campo.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (WINDOW_WIDTH + 100, WINDOW_HEIGHT +200 ))

    titulo = fuente.render("Ingresa tu nombre", True, "black")
    lineas_instrucciones = [
    "Son 4 preguntas a responder ",
    "2 intentos por pregunta para elegir la opcion correcta",
    "m = pausar musica"]

    boton_continuar = crear_boton(450, 620, 200, 70, "white", "Continuar")
    boton_salir = crear_boton(80, 620, 200, 70, "white", "Salir")
    botones = [boton_salir,boton_continuar]

    color_active = "white"
    color_passive = (100, 100, 100) #cambiar
    rect_ingreso = pygame.Rect(470, 100, 220, 40)
    texto_usuario = ''
    texto_activo = False

    resultado = None #para salir al menu, revisar que en modo torneo no se pueda salir porque un jugador cierra el torneo
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_m:
                    entrar_sonido()
                    manejar_musica()
                if texto_activo:
                    if event.key == pygame.K_BACKSPACE:
                        texto_usuario = texto_usuario[:-1]   
                    else:
                        if len(texto_usuario) < 10 and validar_letra(event.unicode):
                            texto_usuario += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if rect_ingreso.collidepoint(event.pos): 
                        texto_activo = True
                    else:
                        texto_activo = False
                    if colision(boton_continuar,event.pos) and len(texto_usuario) > 0:
                        resultado = texto_usuario
                        running = False #pasa a ingreso de nombre
                    if colision(boton_salir,event.pos):
                        running = False

        mx, my = pygame.mouse.get_pos()
        screen.blit(fondo_escalado, (-50,-100))
        screen.blit(titulo, (430,50))
        y = 200
        x = 250
        for linea in lineas_instrucciones:
            superficie_linea = fuente.render(linea, True, "black")
            screen.blit(superficie_linea, (x, y))
            y += 60
        dibujar_botonesd(botones, screen, (mx, my))

        color_nombre = color_active if texto_activo else color_passive #cambiar
        pygame.draw.rect(screen, color_nombre, rect_ingreso)
        superficie_texto = fuente.render(texto_usuario, True, (0, 0, 0))
        screen.blit(superficie_texto, (rect_ingreso.x + 5, rect_ingreso.y + 5))

        pygame.display.flip()
        clock.tick(60) 
    return resultado


def ingresar_jugadores() -> int | None:

    fondo = pygame.image.load("pyjuego/imagenes/campo.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (WINDOW_WIDTH + 100, WINDOW_HEIGHT +200 ))

    titulo = fuente.render("Ingresa cantidad de jugadores", True, "black")
    cantidad = fuente.render("Minimo 1, maximo 10",True, "black")

    boton_continuar = crear_boton(500, 620, 200, 70, "white", "Continuar")
    boton_musica = crear_boton(1100, 620, 150,70, "white", "musica")
    boton_salir = crear_boton(100, 620, 200, 70, "white", "Salir")
    rect_ingreso_numero = pygame.Rect(500, 400, 200, 40)

    cant_jugadores = ''
    numero_activo = False
    botones = [boton_continuar,boton_salir,boton_musica]
    color_active = (255, 255, 255)
    color_passive = (100, 100, 100)

    resultado = None #para salir al menu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if numero_activo:
                    if event.key == pygame.K_BACKSPACE:
                        cant_jugadores = cant_jugadores[:-1]    
                    else:
                        if validar_numero(event.unicode):
                            nuevo = cant_jugadores + event.unicode
                            if nuevo[0] != "0" and 1 <= int(nuevo) <= 10: # chatgpt ass
                                 cant_jugadores = nuevo
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if rect_ingreso_numero.collidepoint(event.pos): 
                        numero_activo = True
                    else:
                        numero_activo = False
                    if colision(boton_continuar, event.pos) and len(cant_jugadores) > 0:
                        resultado = int(cant_jugadores) 
                        running = False # devuelve resultado en vez de pygame.quit y hacer crash
                    if colision(boton_musica, event.pos):
                        entrar_sonido()
                        manejar_musica()
                    if colision(boton_salir, event.pos):
                        salir_sonido()
                        running = False

        screen.blit(fondo_escalado, (-50,-100))
        mx, my = pygame.mouse.get_pos()
        screen.blit(titulo, (350,200))
        screen.blit(cantidad,(420,260))

        color_numero = color_active if numero_activo else color_passive
        pygame.draw.rect(screen, color_numero, rect_ingreso_numero)
        superficie_numero = font.render(cant_jugadores, True, "black")
        screen.blit(superficie_numero, (rect_ingreso_numero.x + 5,rect_ingreso_numero.y + 5))
        dibujar_botonesd(botones, screen, (mx, my))

        pygame.display.flip()
        clock.tick(60)

    return resultado
