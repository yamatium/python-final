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
        pass  # already deleted, nothing to do
    
def puntuacion():
    puntajes = cargar_puntuacion()

    fondo = pygame.image.load("pyjuego/imagenes/arbol.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (WINDOW_WIDTH + 100, WINDOW_HEIGHT +200 ))
    puntuacionVacia = font.render("No hay puntajes todavia, ve a jugar!", True, "black")
    titulo = font.render("Tabla de puntuaciones", True, "black")
    block_borrar = Box(100, 650, 200, 60, "grey", "Borrar historial")
    block_salir = Box(100, 550, 200, 60, "grey", "salir")
    rect_musica = Box(1100, 620, 150,70, "white", "musica")

    block_subir = Box(1000, 130, 60, 50, "gray", "^")
    block_bajar = Box(1000, 600, 60, 50, "gray", "v")
    scroll_offset = 0
    scroll_speed = 40
    lista_area = pygame.Rect(0, 110, WINDOW_WIDTH, 470)

    botones = [block_salir, block_borrar, block_subir, block_bajar, rect_musica]
    
    blocks_puntaje = []
    y = 150
    for p in puntajes:
        texto = f"Jugador: {p['nombre']} | estado final: {p['estado']} | puntaje: {p['puntaje']}"
        box = Box(350, y, 600, 60, "gray", texto,draw_bg=False)
        box.original_y = y
        blocks_puntaje.append(box)
        y += 70

    contenido_alto = len(blocks_puntaje) * 70
    max_scroll = max(0, contenido_alto - lista_area.height)

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
                    if block_borrar.collidepoint(event.pos):
                        block_borrar.sonidoClick("salir")
                        borrar_puntuacion()
                        blocks_puntaje = [] 
                        puntajes = []
                    if block_salir.collidepoint(event.pos):
                        block_salir.sonidoClick("salir")
                        running = False
                    if rect_musica.collidepoint(event.pos):
                        entrar_sonido()
                        manejar_musica()
                    if block_subir.collidepoint(event.pos):
                        scroll_offset -= scroll_speed
                        scroll_offset = max(0, min(scroll_offset, max_scroll))
                    if block_bajar.collidepoint(event.pos):
                        scroll_offset += scroll_speed
                        scroll_offset = max(0, min(scroll_offset, max_scroll))

        mx, my = pygame.mouse.get_pos()
        screen.blit(fondo_escalado, (-50,-100))
        if not puntajes:
           screen.blit(puntuacionVacia,(330,400))

        screen.blit(titulo, (450,90))
        dibujar_botones(botones, screen, (mx, my))
            
        screen.set_clip(lista_area)
        for block in blocks_puntaje:
            block.rect.y = block.original_y - scroll_offset
            block.draw(screen)
        screen.set_clip(None)

        pygame.display.flip()
        clock.tick(60)