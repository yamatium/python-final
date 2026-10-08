import pygame, os

from .configuracion import *
from .diccionarios.boton import *
from .ingresar_datos import *

pantalla = crear_superficie_pantalla()
clock = pygame.time.Clock()
fuente = crear_fuente(50)

def guardar_puntaje(nombre:str, estado_final: bool,puntaje) -> None:
    #guarda el resultado del jugador en un archivo csv
    estado_final = "Completo" if estado_final else "No Completo"
    with open("puntuacion.csv", "a") as archivo:
        archivo.write(f"{nombre},{estado_final},{puntaje}\n")

def ordenar_puntajes(lista:list)->None:
    #ordenar la puntuacion con algoritmo de burbuja
    recorrido = len(lista)

    for i in range(recorrido-1):
        for j in range(recorrido-i-1):
            if lista[j]["puntaje"] < lista[j+1]["puntaje"]:
                temp = lista[j]
                lista[j] = lista[j+1]
                lista[j+1] = temp
    return lista

def cargar_puntuacion()-> list:
    puntuacion = []
    try:
        with open("puntuacion.csv", "r") as archivo:
            for linea in archivo:
                partes = linea.strip().split(",")  # strip saca el \n invisible
                nombre = partes[0]
                estado = partes[1]
                puntaje = int(partes[2]) #casteo str a int
                puntuacion.append({"nombre": nombre, "estado": estado, "puntaje": puntaje}) 
            puntuacion_ordenada = ordenar_puntajes(puntuacion)
    except FileNotFoundError:
        print("Archivo no encontrado")
    return puntuacion_ordenada # devuelve una lista de diccionarios

def borrar_puntuacion() -> None:
    try:
        os.remove("puntuacion.csv")
    except FileNotFoundError:
        pass 

def aplicar_scroll(block, posicion_scroll):
    y_scroll = block["y_base"] - posicion_scroll
    block["rectangulo"].y = y_scroll
    block["texto_rectangulo"].center = block["rectangulo"].center
    return block
    
def puntuacion():
    puntajes = cargar_puntuacion()

    fondo = pygame.image.load("pyjuego/imagenes/arbol.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (WINDOW_WIDTH + 100, WINDOW_HEIGHT +200 ))
    puntuacionVacia = fuente.render("No hay puntajes todavia, ve a jugar!", True, "black")
    titulo = fuente.render("Tabla de puntuaciones", True, "black")
    formato_puntaje = fuente.render("Jugador | estado final | puntaje", True, "black")

    boton_salir = crear_boton(40, 550, 240, 60, "grey", "salir")
    boton_borrar = crear_boton(40, 650, 240, 60, "grey", "borrar tabla")
    boton_musica = crear_boton(1100, 620, 150,70, None, "musica")
    boton_subir = crear_boton(1100, 150, 60, 50, "gray", "^")
    boton_bajar = crear_boton(1100, 500, 60, 50, "gray", "v")

    posicion_scroll = 0 # posicion actual de scroll
    velocidad_scroll = 50 
    lista_area = pygame.Rect(0, 140, 1280, 470) # define el area a usar scrolling, linea 108
    botones = [boton_salir, boton_borrar, boton_subir, boton_bajar, boton_musica]

    #hacer funcion
    blocks_puntaje = []
    y = 170
    for p in puntajes:
        texto = f"{p['nombre']} | {p['estado']} | {p['puntaje']}"
        box = crear_boton(350, y, 700,60,"gray", texto)
        box["y_base"] = y
        blocks_puntaje.append(box)
        y += 70
        

    altura_lista = len(blocks_puntaje) * 80 # altura de lista segun entradas. 70 se corta el ultimo dato
    #max_scroll = max(0, altura_lista - lista_area.height)  # limite de movimiento y de lista 
    max_scroll = (altura_lista - lista_area.height) # it just works!,lineas 96 y 100 resguardan error

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #hacer manejo de evento casero, como menu.py
                    if colision(boton_borrar,event.pos):
                        salir_sonido()
                        borrar_puntuacion()
                        blocks_puntaje = [] 
                        puntajes = []
                    if colision(boton_salir, event.pos):
                        salir_sonido()
                        running = False
                    if colision(boton_musica, event.pos):
                        entrar_sonido()
                        manejar_musica()
                    if colision(boton_subir, event.pos):
                        posicion_scroll -= velocidad_scroll 
                        posicion_scroll = max(0, posicion_scroll)
                        #posicion_scroll = max(0, min(posicion_scroll, max_scroll))#controla que no se suba mas de y
                        #max (0 , (valor minimo/ posible negativo )) es 0 para que no sea negativo y se escape de la lista
                    if colision(boton_bajar, event.pos):
                        posicion_scroll += velocidad_scroll 
                        posicion_scroll = max(0, min(posicion_scroll, max_scroll))#controla que no se baje mas de y
        
        mx, my = pygame.mouse.get_pos()
        pantalla.blit(fondo_escalado, (-50,-100))
        pantalla.blit(titulo, (470,60))
        pantalla.blit(formato_puntaje, (420,100))
        dibujar_botonesd(botones, pantalla, (mx, my))

        if not puntajes:
           pantalla.blit(puntuacionVacia,(330,380))    
        pantalla.set_clip(lista_area) # define el area a usar el scrolling

        for block in blocks_puntaje:
            block = aplicar_scroll(block, posicion_scroll)
            dibujar_botonesd(block, pantalla, (mx, my))
        pantalla.set_clip(None)

        pygame.display.flip()
        clock.tick(60)