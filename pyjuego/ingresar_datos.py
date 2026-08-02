import pygame
from settings import *
from box import *

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

def guardar_puntaje(nombre, estado_final,puntaje):
    estado_final = "Completo" if estado_final else "No Completo"
    with open("puntuacion.txt", "a") as archivo:
        archivo.write(f"Jugador: {nombre} | estado final: {estado_final} | puntaje: {puntaje}\n")

def cargar_puntuacion():
    puntuacion = []
    try:
        with open("puntuacion.txt", "r") as archivo:
            for linea in archivo:
                # "Jugador: b | estado final: Completo | puntaje: 91"
                partes = linea.strip().split(" | ")
                nombre = partes[0].replace("Jugador: ", "")
                estado = partes[1].replace("estado final: ", "")
                puntaje = partes[2].replace("puntaje: ", "")
                puntuacion.append({"nombre": nombre, "estado": estado, "puntaje": puntaje})
    except FileNotFoundError:
        print("Archivo no encontrado")
    return puntuacion


def ingreso_datos():
    rect_nombre = Box(450, 130, 300, 100, "white", "Ingresa tu nombre marico")
    rect_continuar = Box(500, 550, 200, 70, "white", "Continuar")
    color_active = (255, 255, 255)
    color_passive = (100, 100, 100)
    rect_ingreso = pygame.Rect(500, 300, 200, 40)
    texto_usuario = ''
    texto_activo = False
   
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
                    # event.pos es una tupla de la posicion del mouse cuando el evento pasa (x,y)
                    if rect_ingreso.collidepoint(event.pos): 
                        texto_activo = True
                    else:
                        texto_activo = False
                    #if rect_continuar.collidepoint(event.pos) and len(texto_usuario) > 0:
                    #       return texto_usuario # switch to quiz screen
                    if rect_continuar.collidepoint(event.pos) and len(texto_usuario) > 0:
                        return texto_usuario # switch to quiz screen


        screen.fill(COLORS["royalblue"])
        mx, my = pygame.mouse.get_pos()
        rect_nombre.draw(screen)
        rect_continuar.draw(screen)

        color_nombre = color_active if texto_activo else color_passive
        pygame.draw.rect(screen, color_nombre, rect_ingreso)

        superficie_texto = font.render(texto_usuario, True, (0, 0, 0))
        screen.blit(superficie_texto, (rect_ingreso.x + 5, rect_ingreso.y + 5))

        pygame.display.flip()
        clock.tick(60) 


def ingresar_jugadores():

    rect_numero = Box(650, 330, 300, 100, "white", "Ingresa cant jugadores")
    rect_continuar = Box(500, 550, 200, 70, "white", "Continuar")
    rect_ingreso_numero = pygame.Rect(600, 500, 200, 40)
    cant_jugadores = ''
    numero_activo = False
    color_active = (255, 255, 255)
    color_passive = (100, 100, 100)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
                        return int(cant_jugadores) # switch to quiz screen
       
        screen.fill(COLORS["royalblue"])
        mx, my = pygame.mouse.get_pos()
        rect_numero.draw(screen)
        rect_continuar.draw(screen)
        color_numero = color_active if numero_activo else color_passive
        pygame.draw.rect(screen, color_numero, rect_ingreso_numero)
        superficie_numero = font.render(cant_jugadores, True, (0, 0, 0))
        screen.blit(superficie_numero, (rect_ingreso_numero.x + 5,rect_ingreso_numero.y + 5))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
