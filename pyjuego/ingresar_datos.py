import pygame
from configuracion import *
from objetos.box import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)


def validar_letra(caracter, estado="ingreso"):
    
    letras = "abcdefghijklmnopqrstuvwxyz"
    if estado == "ingreso":
        letras = "abcdefghijklmnopqrstuvwxyz"
    else:
        letras = "abcd"
        
    return len(caracter) == 1 and caracter in letras

def validar_numero_parcial(texto_actual, caracter):
    if not caracter.isdigit():
        return False
    texto_resultante = texto_actual + caracter
    valor = int(texto_resultante)
    return valor <= 10


def ingreso_datos():
    fondo = pygame.image.load("pyjuego/imagenes/campo.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (WINDOW_WIDTH + 100, WINDOW_HEIGHT +200 ))

    titulo = font.render("Ingresa tu nombre", True, "black")
    lineas_instrucciones = [
    "Son 4 preguntas",
    "2 intentos por pregunta para elegir la opcion correcta",
    "m = pausar musica",
    "p/barra espaciadora = pausar el juego"]

    rect_continuar = Box(500, 600, 200, 70, "white", "Continuar")
    rect_salir = Box(80, 600, 200, 70, "white", "Salir") # menu pausa para salir a menu principal
    color_active = (255, 255, 255)
    color_passive = (100, 100, 100)
    rect_ingreso = pygame.Rect(450, 100, 200, 40)
    texto_usuario = ''
    texto_activo = False

    resultado = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
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
                    if rect_continuar.collidepoint(event.pos) and len(texto_usuario) > 0:
                        resultado = texto_usuario
                        running = False
                    if rect_salir.collidepoint(event.pos):
                        running = False


        screen.blit(fondo_escalado, (-50,-100))
        screen.blit(titulo, (400,50))
        y = 250
        for linea in lineas_instrucciones:
            superficie_linea = font.render(linea, True, "black")
            screen.blit(superficie_linea, (250, y))
            y += 40
        rect_continuar.draw(screen)
        rect_salir.draw(screen)

        color_nombre = color_active if texto_activo else color_passive
        pygame.draw.rect(screen, color_nombre, rect_ingreso)

        superficie_texto = font.render(texto_usuario, True, (0, 0, 0))
        screen.blit(superficie_texto, (rect_ingreso.x + 5, rect_ingreso.y + 5))

        pygame.display.flip()
        clock.tick(60) 
    return resultado


def ingresar_jugadores():

    fondo = pygame.image.load("pyjuego/imagenes/campo.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (WINDOW_WIDTH + 100, WINDOW_HEIGHT +200 ))

    titulo = font.render("Ingresa cantidad de jugadores", True, "black")
    cantidad = font.render("Minimo 1, maximo 10",True, "black")

    rect_continuar = Box(500, 600, 200, 70, "white", "Continuar")
    rect_musica = Box(100, 600, 150,70, "white", "musica")
    rect_salir = Box(100, 550, 200, 70, "white", "Salir")
    rect_ingreso_numero = pygame.Rect(500, 400, 200, 40)

    cant_jugadores = ''
    numero_activo = False
    color_active = (255, 255, 255)
    color_passive = (100, 100, 100)

    resultado = None # None = cancelado / volver al menu
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
                        if len(cant_jugadores) < 2 and validar_numero_parcial(cant_jugadores, event.unicode):
                            cant_jugadores += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # event.pos es una tupla de la posicion del mouse cuando el evento pasa (x,y)
                    if rect_ingreso_numero.collidepoint(event.pos): 
                        numero_activo = True
                    else:
                        numero_activo = False
                    if rect_continuar.collidepoint(event.pos) and len(cant_jugadores) > 0:
                        resultado = int(cant_jugadores) 
                        running = False # devuelve resultado en vez de pygame.quit y hacer crash
                    if rect_musica.collidepoint(event.pos):
                        entrar_sonido()
                        manejar_musica()
                    if rect_salir.collidepoint(event.pos):
                        running = False

        screen.blit(fondo_escalado, (-50,-100))
        mx, my = pygame.mouse.get_pos()
        screen.blit(titulo, (350,200))
        screen.blit(cantidad,(420,260))

        rect_continuar.draw(screen)
        rect_salir.draw(screen)
        color_numero = color_active if numero_activo else color_passive

        pygame.draw.rect(screen, color_numero, rect_ingreso_numero)
        superficie_numero = font.render(cant_jugadores, True, "black")
        screen.blit(superficie_numero, (rect_ingreso_numero.x + 5,rect_ingreso_numero.y + 5))

        pygame.display.flip()
        clock.tick(60)

    return resultado
