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

def ingreso_datos():
    rect_nombre = Box(450, 130, 300, 100, "white", "Ingresa tu nombre marico")
    rect_numero = Box(650, 330, 300, 100, "white", "Ingresa cant jugadores")
    rect_continuar = Box(500, 550, 200, 70, "white", "Continuar")
    color_active = (255, 255, 255)
    color_passive = (100, 100, 100)
    rect_ingreso = pygame.Rect(500, 300, 200, 40)
    texto_usuario = ''
    texto_activo = False

    rect_ingreso_numero = pygame.Rect(600, 500, 200, 40)
    texto_numero = ''
    numero_activo = False
   
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
                elif numero_activo:
                    if event.key == pygame.K_BACKSPACE:
                        texto_numero = texto_numero[:-1]
                    else:
                        if len(texto_numero) < 2 and validar_numero_parcial(texto_numero, event.unicode):
                            texto_numero += event.unicode     

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # event.pos es una tupla de la posicion del mouse cuando el evento pasa (x,y)
                    if rect_ingreso.collidepoint(event.pos): 
                        texto_activo = True
                        numero_activo = False
                    elif rect_ingreso_numero.collidepoint(event.pos):
                        texto_activo = False
                        numero_activo = True
                    else:
                        texto_activo = False
                        numero_activo = False
                    #if rect_continuar.collidepoint(event.pos) and len(texto_usuario) > 0:
                    #       return texto_usuario # switch to quiz screen
                    if rect_continuar.collidepoint(event.pos) and len(texto_usuario) > 0:
                        return texto_usuario, texto_numero # switch to quiz screen


        screen.fill(COLORS["royalblue"])
        mx, my = pygame.mouse.get_pos()
        rect_nombre.draw(screen)
        rect_numero.draw(screen)
        rect_continuar.draw(screen)

        color_nombre = color_active if texto_activo else color_passive
        color_numero = color_active if numero_activo else color_passive
        pygame.draw.rect(screen, color_nombre, rect_ingreso)
        pygame.draw.rect(screen, color_numero, rect_ingreso_numero)

        superficie_texto = font.render(texto_usuario, True, (0, 0, 0))
        superficie_numero = font.render(texto_numero, True, (0, 0, 0))
        screen.blit(superficie_texto, (rect_ingreso.x + 5, rect_ingreso.y + 5))
        screen.blit(superficie_numero, (rect_ingreso_numero.x + 5,rect_ingreso_numero.y + 5))

        pygame.display.flip()
        clock.tick(60) 
