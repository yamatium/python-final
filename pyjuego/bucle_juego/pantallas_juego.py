import pygame,sys

from pyjuego.configuracion import *
from pyjuego.diccionarios.boton import *
from pyjuego.sonidos.manejo_sonido import *

pantalla = crear_superficie_pantalla()
clock = pygame.time.Clock()
fuente = crear_fuente(50) 

def respuesta_correcta() -> None:
    #dibuja la animacion de respuesta correcta al responder bien una pregunta

    boton_musica = crear_boton(1100, 620, 150,70, None, "musica")
    boton_salir = crear_boton(450, 600, 300,80,"white", "continuar")
    botones = [boton_musica,boton_salir]
    bien = pygame.image.load("pyjuego/imagenes/thumbs-up.png").convert()
    bien_scale = pygame.transform.scale(bien, (498,390))
    #convert cuando no necesitas transparencia, convert_alpha cuando si
    fondo_puerta = pygame.image.load("pyjuego/imagenes/doorTrans.png").convert_alpha()
    fondo_real = pygame.image.load("pyjuego/imagenes/campo2.png").convert()
    fondo_scale = pygame.transform.scale(fondo_puerta, (1500,700))

    puerta_izquierda = pygame.image.load("pyjuego/imagenes/door2.png").convert_alpha()
    izquierda_scale = pygame.transform.scale(puerta_izquierda, (300,450))
    puerta_derecha = pygame.image.load("pyjuego/imagenes/door1.png").convert_alpha()
    derecha_scale = pygame.transform.scale(puerta_derecha, (300,450))

    mensaje = fuente.render("Respuesta Correcta!", True, "black")

    x = 305
    z = 600
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if colision(boton_salir,event.pos):
                        running = False
                    if colision(boton_musica, event.pos):
                        entrar_sonido()
                        manejar_musica()

        mx, my = pygame.mouse.get_pos()
        pantalla.blit(fondo_real, (0,0))
        pantalla.blit(bien_scale, (340,160))
        pantalla.blit(mensaje, (410,120))
        pantalla.blit(fondo_scale, (-100, -120))
        pantalla.blit(izquierda_scale, (x,100))
        pantalla.blit(derecha_scale, (z,100))

        dibujar_botones(botones,pantalla,(mx,my))
        x -= 0.6
        z += 0.6
        
        pygame.display.flip()
        clock.tick(60)


def encontrar_sala_1(lista:list)-> list:
    #agrega a una lista los nombres de quienes no pasaron la sala 1
    sala_1 = []

    for diccionario in lista:
        if diccionario["salas"] < 2 :
            sala_1.append(diccionario["nombre"])
    return sala_1

def encontrar_maximo(lista:list)-> int:
    #encuentra el puntaje maximo entre los resultados
    maximo = 0
    for diccionario in lista:
        puntaje = diccionario["puntuacion"]
        if puntaje > maximo:
            maximo = puntaje
    return  maximo

def encontrar_puntaje_ganadores(resultados: list, puntaje_maximo:int)-> list:
    #encuentra los nombres de los jugadores con maximo puntaje
    ganadores = []
    for jugadores in resultados:
        if jugadores["puntuacion"] == puntaje_maximo:
            ganadores.append(jugadores["nombre"])
    return ganadores

def encontrar_sala_maxima(resultados:list)-> int:
    #encuentra la sala maxima jugada
    maximo = 1
    for salas in resultados:
        sala = salas["salas"]
        if sala > maximo:
            maximo = sala
    return maximo

def encontrar_ganadores_sala(resultados:list, sala_maxima:int)-> list:
    #encuentra los jugadores con mayor salas ganadas
    ganadores_sala = []
    for jugador in resultados:
        if jugador["salas"] == sala_maxima:
            ganadores_sala.append(jugador["nombre"])
    return ganadores_sala

def formatear_nombres(jugadores:list) -> str:
    #formatea la lista de jugadores para usar en los mensajes 
    #agrega una coma antes de agregar el nombre
    mensaje = ""
    separador = ", "
    for i in range(len(jugadores)):
        if i > 0:
            mensaje += separador
        mensaje += jugadores[i]
    return mensaje

def mensaje_sala_1(eliminados_sala:list)-> pygame.Surface:
    #crea el texto de mensaje de sala 1 para dibujar
    if eliminados_sala:
        nombres = formatear_nombres(eliminados_sala)
        mensaje_eliminados = fuente.render(f"No superaron sala 1: {(nombres)}", True, "red")
    else:
        mensaje_eliminados = fuente.render("Todos superaron la sala 1!", True, "green")
    return mensaje_eliminados

def mensaje_mayor_puntaje(puntaje_maximo:int, ganadores_puntaje:list) -> pygame.Surface:
    nombres = formatear_nombres(ganadores_puntaje)
    return fuente.render(f"Mayor puntaje ({puntaje_maximo} pts): {nombres}", True, "yellow")

def mensaje_mayor_sala(sala_maxima:int, ganadores:list)-> pygame.Surface:
    nombres = formatear_nombres(ganadores)
    return fuente.render(f"Llegaron mas lejos (sala {sala_maxima}): {nombres}", True, "aqua")

#funciones duplicadas: encontrar_maximo / encontrar_sala_maxima y 
# encontrar_puntaje_ganadores / encontrar_ganadores_sala son la misma logica con diferentes llaves.

def mostrar_torneo(resultados:list) -> None:

    fondo = pygame.image.load("pyjuego/imagenes/forest.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (1380, 920 ))
    boton_musica = crear_boton(1100, 620, 150,70, "white", "musica")
    boton_salir = crear_boton(400, 600, 450,100,"white", "Salir")

    botones = [boton_musica,boton_salir]

    puntaje_maximo = encontrar_maximo(resultados)
    ganadores_puntaje = encontrar_puntaje_ganadores(resultados,puntaje_maximo)
    sala_maxima = encontrar_sala_maxima(resultados)
    ganadores_salas = encontrar_ganadores_sala(resultados,sala_maxima)
    eliminados_sala = encontrar_sala_1(resultados)
    #https://www.pygame.org/docs/ref/color_list.html
    titulo = fuente.render("Resultados del Torneo", True, "white")
    #ganadores_sala_maxima = formatear_nombres(ganadores_salas)
    puntaje = mensaje_mayor_puntaje(puntaje_maximo,ganadores_puntaje)
    sala = mensaje_mayor_sala(sala_maxima,ganadores_salas)
    texto = mensaje_sala_1(eliminados_sala)

    dibujar = [titulo,puntaje,sala,texto]
    posiciones = [(380, 40),(380, 240),(380, 290),(380, 340)]  

    # --- pantalla de resultados ---
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if colision(boton_salir, event.pos):
                        running = False
                    if colision(boton_musica, event.pos):
                        entrar_sonido()
                        manejar_musica()

        pantalla.blit(fondo_escalado, (-50,-100))
        mx, my = pygame.mouse.get_pos()
        for i in range(len(dibujar)):
            pantalla.blit(dibujar[i], (posiciones[i]))
        dibujar_botones(botones,pantalla,(mx,my))

        pygame.display.flip()
        clock.tick(60)