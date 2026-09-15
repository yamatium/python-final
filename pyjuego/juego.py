import pygame
import random

from puntuacion import *
from configuracion import *
from objetos.Caja import Caja
from objetos.dibujar_Resultados import *
from objetos.temporizador import *
from pantallas_juego import *

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

def responder_pregunta(respuesta:str):
    respuesta_final = respuesta
    return respuesta_final

def limpiar_respuesta():
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

def jugar():
    color_activo = (255, 255, 255)
    color_pasivo = (100, 100, 100)
    tabla_resultados = dibujar_Resultados(200,320,200,50)
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
    texto_activo = False
    respuesta = ""
    respuesta_final = ""

    #definir rectangulos para usar con  variables
    rect_ingreso = pygame.Rect(500, 580, 200, 40)
    rect_responder = Caja(500, 630, 200, 70, "white", "Continuar")
    boton_salir = Caja(480, 610, 250,80,"white", "Salir")
    puntuacion_actual = font.render(f"puntaje: {puntuacion}", True, "black")
    intentos_actual = font.render(f"Intentos: {intentos}", True, "black")
    mensaje_final = font.render("Juego terminado", True, "black")

    tiempo = Temporizador(20)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_RETURN:
                    respuesta_final = responder_pregunta(respuesta)
                    respuesta = limpiar_respuesta()
                elif event.key == pygame.K_m:
                    entrar_sonido()
                    manejar_musica()
                if texto_activo:
                    if event.key == pygame.K_BACKSPACE:
                        respuesta = respuesta[:-1]
                    else:
                        if len(respuesta) < 1 and validar_letra(event.unicode, "juego"):
                            respuesta += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not juego_terminado:
                    texto_activo = rect_ingreso.collidepoint(event.pos)
                    if rect_responder.collidepoint(event.pos):
                        respuesta_final = responder_pregunta(respuesta)
                        respuesta = limpiar_respuesta()
                else:
                    if boton_salir.collidepoint(event.pos):
                        running = False

        screen.blit(fondo_escalado, (-50,-100))
        mx, my = pygame.mouse.get_pos()
        color_nombre = color_activo if texto_activo else color_pasivo
        tiempo.actualizar()
        
        if not juego_terminado:
            # --- pantalla de cuestionario ---
                dibujar_pregunta(pregunta_formateada,400,50)
                screen.blit(puntuacion_actual, (2, 400))
                screen.blit(intentos_actual,(2,100))

                dibujar_opciones(screen, pregunta_aleatoria)
                tiempo.dibujar(screen)

                pygame.draw.rect(screen, color_nombre, rect_ingreso)
                superficie_texto = font.render(respuesta, True, (0, 0, 0))
                screen.blit(superficie_texto, (rect_ingreso.x + 5, rect_ingreso.y + 5))
                dibujar_botones(rect_responder, screen, (mx, my))
                
                if respuesta_final == preguntas[pregunta_aleatoria]["respuesta"]:
                    puntuacion += preguntas[pregunta_aleatoria]["valor_puntaje"]
                    preguntas_correctas += 1
                    respuesta_final = ""
                    respuesta_correcta()

                    tabla_resultados.agregar_resultado(
                        nombre_sala=f"Sala {sala}",
                        puntaje_sala= preguntas[pregunta_aleatoria]["valor_puntaje"],
                        puntaje_total= puntuacion
                        )

                    if preguntas_correctas >= 4 :
                        juego_terminado = True
                        estado_final = True
                        guardar_puntaje(nombre_jugador,estado_final,puntuacion)
                        
                    else:   
                        pregunta_aleatoria = random.choice(list(preguntas.keys()))
                        pregunta_formateada = formatear_texto(preguntas[pregunta_aleatoria]["pregunta"])
                        dibujar_pregunta(pregunta_formateada,400,50)
                        dibujar_opciones(screen, pregunta_aleatoria)
                        pygame.draw.rect(screen, color_nombre, rect_ingreso)
                        screen.blit(superficie_texto, (rect_ingreso.x + 5, rect_ingreso.y + 5))
                        intentos = 2
                        sala +=1
                        tiempo.resetear()

                elif respuesta_final != "" and respuesta_final != preguntas[pregunta_aleatoria]["respuesta"]:
                    intentos -= 1
                    print(f"incorrecto intentos: {intentos}")
                    respuesta_final = ""

                if intentos < 1 or tiempo.terminado:
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
            tabla_resultados.dibujar(screen,font)
            dibujar_botones(boton_salir, screen, (mx, my))
            
        pygame.display.flip()
        clock.tick(60)

    resultados = {"nombre": nombre_jugador, "puntuacion": puntuacion, "salas": sala, "gano": estado_final}
    return resultados

