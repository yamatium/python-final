import pygame
import random

from .puntuacion import *
from .configuracion import *

from .pantallas_juego import *
from .diccionarios.boton import *
from .diccionarios.cronometro import *
from .diccionarios.resultados_juego import *

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def dibujar_opciones(screen, pregunta_aleatoria) -> None:
    opciones = preguntas[pregunta_aleatoria]["opciones"]
    posiciones = [(250, 330), (650, 330), (250, 430), (650, 430)]

    for i in range(4):
        fuente_opcion = font.render(opciones[i], True, "black")
        x, y = posiciones[i]
        screen.blit(fuente_opcion, (x, y))

def dibujar_estado(nombre, estado_final) -> list: # dibuja al final de la partida
    nombre = font.render(f"Jugador: {nombre}", True, "black")
    if estado_final:
        final = font.render("Ganaste!", True, "black")
    else:
        final = font.render("Perdiste!", True, "black")

    resultado = [nombre ,final]
    return resultado

def responder_pregunta(respuesta:str)-> str:
    respuesta_final = respuesta
    return respuesta_final

def limpiar_respuesta()->str:
    respuesta = ""
    return respuesta

def formatear_texto(texto):
    lineas = texto.split(",")
    return lineas

def dibujar_pregunta(pregunta, x,y) :
    for linea in pregunta:
        linea = font.render(linea, True, "black")
        screen.blit(linea, (x, y))
        y += 60

def crear_botones_opciones(pregunta_aleatoria) -> list:
    cantidad = 4
    lista = []
    opciones = preguntas[pregunta_aleatoria]["opciones"]
    posiciones = [(250, 400), (700, 400), (250, 510), (700, 510)]
    ancho = 150
    alto = 100

    for i in range(cantidad):
        x,y = posiciones[i]
        boton = crear_boton(x,y,ancho,alto, None, opciones[i])
        lista.append(boton)
    return lista
 

def jugar():
    resultados = crear_resultados(200,320,200,50)
    #imagenes
    fondo = pygame.image.load("pyjuego/imagenes/castle2.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (WINDOW_WIDTH + 100, WINDOW_HEIGHT +200 ))

    nombre_jugador = ingreso_datos() # llama al ingreso de datos loop, regresa el nombre y continua al loop principal
    if nombre_jugador is None:
        return None

    # definir pregunta, opciones  y variantes
    pregunta_aleatoria = random.choice(list(preguntas.keys()))
    pregunta_formateada = formatear_texto(preguntas[pregunta_aleatoria]["pregunta"])
    dibujar_pregunta(pregunta_formateada,400,50)
    dibujar_opciones(screen, pregunta_aleatoria)

    juego_terminado = False
    puntuacion = 0
    preguntas_correctas = 0
    sala = 1
    intentos = 2
    estado_final = False
    respuesta = ""
    respuesta_final = ""

    #definir botones
    boton_salir = crear_boton(480, 610, 250,80,"white", "Salir")
    botones = crear_botones_opciones(pregunta_aleatoria)

    puntuacion_actual = font.render(f"puntaje: {puntuacion}", True, "black")
    intentos_actual = font.render(f"Intentos: {intentos}", True, "black")
    mensaje_final = font.render("Juego terminado", True, "black")

    cronometro = crear_cronometro(20)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_m:
                    entrar_sonido()
                    manejar_musica()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not juego_terminado:
                    if colision(botones[0], event.pos):
                        respuesta = botones[0]["texto"][0]
                        print(botones[0]["texto"][0]) #["texto"][0] saca solo a,b,c o d respectivamente
                        respuesta_final = responder_pregunta(respuesta)
                    if colision(botones[1], event.pos):
                        respuesta = botones[1]["texto"][0]
                        print(botones[1]["texto"][0]) #["texto"][0] saca solo a,b,c o d respectivamente
                        respuesta_final = responder_pregunta(respuesta)
                    if colision(botones[2], event.pos):
                        respuesta = botones[2]["texto"][0]
                        print(botones[2]["texto"][0]) #["texto"][0] saca solo a,b,c o d respectivamente
                        respuesta_final = responder_pregunta(respuesta)
                    if colision(botones[3], event.pos):
                        respuesta = botones[3]["texto"][0]
                        print(botones[3]["texto"][0]) #["texto"][0] saca solo a,b,c o d respectivamente
                        respuesta_final = responder_pregunta(respuesta)
                else:
                    if colision(boton_salir, event.pos):
                        running = False

        screen.blit(fondo_escalado, (-50,-100))
        mx, my = pygame.mouse.get_pos()
        actualizar_tiempo(cronometro)
        
        if not juego_terminado:
            # --- pantalla de cuestionario ---
                dibujar_pregunta(pregunta_formateada,400,50)
                screen.blit(puntuacion_actual, (2, 400))
                screen.blit(intentos_actual,(2,100))

                dibujar_botonesd(botones,screen, (mx,my))
                dibujar_cronometro(cronometro,screen)
                
                if respuesta_final == preguntas[pregunta_aleatoria]["respuesta"]:
                    puntuacion += preguntas[pregunta_aleatoria]["valor_puntaje"]
                    preguntas_correctas += 1
                    respuesta_final = ""
                    respuesta_correcta()

                    puntaje_total = puntuacion
                    completar_resultados(resultados,sala,preguntas[pregunta_aleatoria]["valor_puntaje"],puntaje_total)

                    if preguntas_correctas >= 4 :
                        juego_terminado = True
                        estado_final = True
                        guardar_puntaje(nombre_jugador,estado_final,puntuacion)
                        
                    else:   
                        pregunta_aleatoria = random.choice(list(preguntas.keys()))
                        pregunta_formateada = formatear_texto(preguntas[pregunta_aleatoria]["pregunta"])
                        dibujar_pregunta(pregunta_formateada,400,50)
                        botones = crear_botones_opciones(pregunta_aleatoria)
                        dibujar_botonesd(botones,screen, (mx,my))
                        intentos = 2
                        sala +=1
                        resetear_cronometro(cronometro)

                elif respuesta_final != "" and respuesta_final != preguntas[pregunta_aleatoria]["respuesta"]:
                    intentos -= 1
                    print(f"incorrecto intentos: {intentos}")
                    respuesta_final = ""

                if intentos < 1 or cronometro["tiempo_terminado"]:
                    juego_terminado = True
                    estado_final = False
                    guardar_puntaje(nombre_jugador,estado_final,puntuacion)
                    
                puntuacion_actual = font.render(f"puntaje: {puntuacion}", True, "black")
                intentos_actual = font.render(f"Intentos: {intentos}", True, "black")  
                screen.blit(puntuacion_actual, (2, 400))
                screen.blit(intentos_actual,(2,100))
                

        else:
            screen.blit(mensaje_final, (480,50))
            resultado_jugador = dibujar_estado(nombre_jugador,estado_final)
            screen.blit(resultado_jugador[0], (500,100))
            screen.blit(resultado_jugador[1], (540,180))
            dibujar_resultados(resultados,screen)
            dibujar_botonesd(boton_salir, screen, (mx, my))
            
        pygame.display.flip()
        clock.tick(60)

    resultados = {"nombre": nombre_jugador, "puntuacion": puntuacion, "salas": sala, "gano": estado_final}
    return resultados

