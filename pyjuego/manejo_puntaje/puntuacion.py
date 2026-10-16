import pygame, os

from pyjuego.configuracion import *
from pyjuego.diccionarios.boton import *
from pyjuego.ingresar_datos import *
from pyjuego.sonidos.manejo_sonido import *

pantalla = crear_superficie_pantalla()
clock = pygame.time.Clock()
fuente = crear_fuente(50)

def guardar_puntaje(nombre:str, estado_final: bool,puntaje) -> None:
    #guarda el resultado del jugador en un archivo csv
    estado_final = "Completo" if estado_final else "No Completo"
    with open("pyjuego/manejo_puntaje/puntuacion.csv", "a") as archivo:
        archivo.write(f"{nombre},{estado_final},{puntaje}\n")

def ordenar_puntajes(lista:list)-> list:
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
    # transforma el csv en una lista y algoritmo de burbuja para ordenar los puntajes
    puntuacion = []
    try:
        with open("pyjuego/manejo_puntaje/puntuacion.csv", "r") as archivo:
            for linea in archivo:
                partes = linea.strip().split(",")  # strip saca el \n invisible
                nombre = partes[0]
                estado = partes[1]
                puntaje = int(partes[2]) 
                puntuacion.append({"nombre": nombre, "estado": estado, "puntaje": puntaje}) 
    except FileNotFoundError:
        print("Archivo no encontrado")
    return ordenar_puntajes(puntuacion) # devuelve una lista de diccionarios

def borrar_puntuacion() -> None:
    try:
        os.remove("pyjuego/manejo_puntaje/puntuacion.csv")
    except FileNotFoundError:
        pass 

def aplicar_scroll(block:dict, posicion_scroll:int) -> dict:
    #cambia la posicion de las puntuacion segun el boton de scroleo(arriba o abajo)
    y_scroll = block["y_base"] - posicion_scroll
    block["rectangulo"].y = y_scroll
    block["texto_rectangulo"].center = block["rectangulo"].center
    return block

def crear_rectangulos_puntuacion(puntajes:list) -> list:
    #crea una lista de botones con los datos de puntajes
    botones_puntaje = []
    y = 170
    for p in puntajes:
        texto = f"{p['nombre']} | {p['estado']} | {p['puntaje']}"
        box = crear_boton(350, y, 700,60,"gray", texto)
        box["y_base"] = y
        botones_puntaje.append(box)
        y += 70
    return botones_puntaje

def valor_maximo(a:int,b:int)-> int:
    #busca el maximo entre 2 int
    maximo = 0
    if a > b:
        maximo = a
    else:
        maximo = b
    return maximo

def valor_minimo(a:int,b:int)-> int:
    #busca el minimo entre 2 int
    minimo = 0
    if a < b:
        minimo = a
    else:
        minimo = b
    return minimo
    
def puntuacion()-> None:

    fondo = pygame.image.load("pyjuego/imagenes/arbol.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (1380, 920 ))
    puntuacionVacia = fuente.render("No hay puntajes todavia, ve a jugar!", True, "black")
    titulo = fuente.render("Tabla de puntuaciones", True, "black")
    formato_puntaje = fuente.render("Jugador | estado final | puntaje", True, "black")

    boton_salir = crear_boton(40, 550, 240, 60, "grey", "salir")
    boton_borrar = crear_boton(40, 650, 240, 60, "grey", "borrar tabla")
    boton_musica = crear_boton(1100, 620, 150,70, None, "musica")
    boton_subir = crear_boton(1100, 150, 60, 50, "gray", "^")
    boton_bajar = crear_boton(1100, 500, 60, 50, "gray", "v")

    posicion_scroll = 0 # posicion actual de scroll
    velocidad_scroll = 50 # posicion y que se cambia
    lista_area = pygame.Rect(0, 140, 1280, 470) # define el area a usar scrolling, linea 108
    botones = [boton_salir, boton_borrar, boton_subir, boton_bajar, boton_musica]

    puntajes = cargar_puntuacion()
    botones_puntaje = crear_rectangulos_puntuacion(puntajes)
        
    altura_lista = len(botones_puntaje) * 80 # altura de lista segun entradas. 70 se corta el ultimo dato
    max_scroll = (altura_lista - lista_area.height) # it just works!,lineas 96 y 100 resguardan error

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    #hacer manejo de evento casero, como menu.py
                    if colision(boton_borrar,event.pos):
                        salir_sonido()
                        borrar_puntuacion()
                        botones_puntaje = [] 
                        puntajes = []
                    if colision(boton_salir, event.pos):
                        salir_sonido()
                        running = False
                    if colision(boton_musica, event.pos):
                        entrar_sonido()
                        manejar_musica()
                    if colision(boton_subir, event.pos):
                        posicion_scroll -= velocidad_scroll 
                        posicion_scroll = valor_maximo(0,posicion_scroll)#controla que no se suba mas de y
                        #es 0 para que no sea negativo y se escape de la lista
                    if colision(boton_bajar, event.pos):
                        posicion_scroll += velocidad_scroll
                        minimo = valor_minimo(posicion_scroll, max_scroll)
                        posicion_scroll = valor_maximo(0, minimo)#controla que no se baje mas de y
        
        mx, my = pygame.mouse.get_pos()
        pantalla.blit(fondo_escalado, (-50,-100))
        pantalla.blit(titulo, (470,60))
        pantalla.blit(formato_puntaje, (420,100))
        dibujar_botones(botones, pantalla, (mx, my))

        if not puntajes:
           pantalla.blit(puntuacionVacia,(330,380))    

        pantalla.set_clip(lista_area) # define el area a usar el scrolling,dibuja los puntajes

        for block in botones_puntaje:
            block = aplicar_scroll(block, posicion_scroll)
            dibujar_botones(block, pantalla, (mx, my))

        pantalla.set_clip(None)# saca la restriccion de superficie para que todos los otros elementos se puedan redibujar en cada frame

        pygame.display.flip()
        clock.tick(60)