import pygame, os

from configuracion import *
from objetos.box import Box
from ingresar_datos import *

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def guardar_puntaje(nombre, estado_final,puntaje):
    estado_final = "Completo" if estado_final else "No Completo"
    with open("puntuacion.txt", "a") as archivo:
        archivo.write(f"Jugador: {nombre} | estado final: {estado_final} | puntaje: {puntaje}\n")

def obtener_puntaje(p): # para ordenar puntuacion al cargarlos 
    return int(p["puntaje"])

def cargar_puntuacion():
    puntuacion = []
    try:
        with open("puntuacion.txt", "r") as archivo:
            for linea in archivo:
                # "Jugador: b | estado final: Completo | puntaje: 91"
                partes = linea.strip().split(" | ")  # strip saca el \n invisible
                nombre = partes[0].replace("Jugador: ", "")
                estado = partes[1].replace("estado final: ", "")
                puntaje = partes[2].replace("puntaje: ", "")
                puntuacion.append({"nombre": nombre, "estado": estado, "puntaje": puntaje}) # lo append como diccionario
                #{"nombre": "b",    "estado": "Completo",   "puntaje": "91"}
                puntuacion.sort(key=obtener_puntaje, reverse=True)
    except FileNotFoundError:
        print("Archivo no encontrado")
    return puntuacion

def borrar_puntuacion():
    try:
        os.remove("puntuacion.txt")
    except FileNotFoundError:
        pass 
    
def puntuacion():
    puntajes = cargar_puntuacion()

    fondo = pygame.image.load("pyjuego/imagenes/arbol.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (WINDOW_WIDTH + 100, WINDOW_HEIGHT +200 ))
    puntuacionVacia = font.render("No hay puntajes todavia, ve a jugar!", True, "black")
    titulo = font.render("Tabla de puntuaciones", True, "black")

    boton_borrar = Box(100, 650, 200, 60, "grey", "Borrar historial")
    boton_salir = Box(100, 550, 200, 60, "grey", "salir")
    boton_musica = Box(1100, 620, 150,70, "white", "musica")
    boton_subir = Box(1100, 150, 60, 50, "gray", "^")
    boton_bajar = Box(1100, 500, 60, 50, "gray", "v")
    posicion_scroll = 0 # posicion actual de scroll
    velocidad_scroll = 50 
    lista_area = pygame.Rect(0, 140, 1280, 470) # define el area a usar scrolling, linea 108
    botones = [boton_salir, boton_borrar, boton_subir, boton_bajar, boton_musica]
    
    blocks_puntaje = []
    y = 170
    for p in puntajes:
        texto = f"Jugador: {p['nombre']} | estado final: {p['estado']} | puntaje: {p['puntaje']}"
        box = Box(350, y, 700, 60, "gray", texto)
        box.original_y = y
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
                    if boton_borrar.collidepoint(event.pos):
                        boton_borrar.sonidoClick("salir")
                        borrar_puntuacion()
                        blocks_puntaje = [] 
                        puntajes = []
                    if boton_salir.collidepoint(event.pos):
                        boton_salir.sonidoClick("salir")
                        running = False
                    if boton_musica.collidepoint(event.pos):
                        entrar_sonido()
                        manejar_musica()
                    if boton_subir.collidepoint(event.pos):
                        posicion_scroll -= velocidad_scroll 
                        posicion_scroll = max(0, posicion_scroll)
                        #posicion_scroll = max(0, min(posicion_scroll, max_scroll))#controla que no se suba mas de y
                        #max (0 , (valor minimo/ posible negativo )) es 0 para que no sea negativo y se escape de la lista
                    if boton_bajar.collidepoint(event.pos):
                        posicion_scroll += velocidad_scroll 
                        posicion_scroll = max(0, min(posicion_scroll, max_scroll))#controla que no se baje mas de y
        
        mx, my = pygame.mouse.get_pos()
        screen.blit(fondo_escalado, (-50,-100))
        screen.blit(titulo, (450,90))
        dibujar_botones(botones, screen, (mx, my))

        if not puntajes:
           screen.blit(puntuacionVacia,(330,400))    
        screen.set_clip(lista_area) # define el area a usar el scrolling
        for block in blocks_puntaje:
            block.rect.y = block.original_y - posicion_scroll
            block.draw(screen)
        screen.set_clip(None)

        pygame.display.flip()
        clock.tick(60)