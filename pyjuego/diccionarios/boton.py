from pyjuego.configuracion import *

def crear_fuente():
    tamanio = 50
    fuente = pygame.font.SysFont(None, tamanio)
    return fuente

def crear_superficie_texto(texto, fuente):
    texto_superficie = fuente.render(texto, True, "black")
    return texto_superficie

def crear_rectangulo(x, y, ancho, alto):
    rectangulo = pygame.Rect(x, y, ancho, alto)  # define rect first
    return rectangulo

def traer_rectangulo_texto(superficie, rect_boton):
    texto_rectangulo = superficie.get_rect(center=rect_boton.center)
    return texto_rectangulo


def formatear_diccionario(x:int, y:int, ancho:int, alto:int, color:str, texto:str,rectangulo, superficie,texto_rectangulo)-> dict:
    boton = {}
    boton["x"] = x
    boton["y"] = y
    boton["ancho"] = ancho
    boton["alto"] = alto
    boton["color"] = color
    boton["color_constante"] = color
    boton["texto"] = texto
    boton["rectangulo"] = rectangulo
    boton["superficie"] = superficie
    boton["texto_rectangulo"] = texto_rectangulo
    return boton


def crear_boton(x:int, y:int, ancho:int, alto:int, color:str, texto:str) -> dict:
    fuente = crear_fuente()
    rectangulo = crear_rectangulo(x,y,ancho,alto)
    superficie_texto = crear_superficie_texto(texto, fuente)

    texto_rectangulo = traer_rectangulo_texto(superficie_texto, rectangulo)
    boton = formatear_diccionario(x, y, ancho, alto, color, texto,rectangulo, superficie_texto,texto_rectangulo)
    return boton

def colision(boton,pos):
    return boton["rectangulo"].collidepoint(pos)

def dibujar_boton(boton:dict,color ,superficie):
    if color:
        pygame.draw.rect(superficie, color, boton["rectangulo"])
    superficie.blit(boton["superficie"], boton["texto_rectangulo"])

def dibujar_botonesd(botones, screen, mouse_pos):
    if type(botones) == list: # revisa que sea una lista
            for boton in botones:
                boton["color"] = COLORS["lightblue"] if colision(boton,mouse_pos) else boton["color_constante"] # boton.contante es el color hardcodeado, sino boton.color cambia 
                dibujar_boton(boton,boton["color"],screen)
    else: 
        botones["color"] = COLORS["lightblue"] if colision(botones,mouse_pos) else botones["color_constante"]
        dibujar_boton(botones,botones["color"],screen)


