import pygame, sys
import random

from pyjuego.manejo_puntaje.puntuacion import guardar_puntaje
from .pantallas_juego import respuesta_correcta
from pyjuego.sonidos.manejo_sonido import entrar_sonido, manejar_musica
from pyjuego.configuracion import *  #otros modulos con * traen a configuracion al ser importados, ya que estan importando configuracion
from pyjuego.diccionarios.boton import *
from pyjuego.diccionarios.cronometro import *
from pyjuego.diccionarios.resultados_juego import *
from .dibujar_elementos import *


def manejo_click(botones:list,posicion:tuple)-> str:
        #manejo de botones al hacer click 
    respuesta = ""
    if colision(botones[0], posicion):
        respuesta = botones[0]["texto"][0]
        print(botones[0]["texto"][0]) #["texto"][0] saca solo a,b,c o d respectivamente
    if colision(botones[1], posicion):
        respuesta = botones[1]["texto"][0]
    if colision(botones[2], posicion):
        respuesta = botones[2]["texto"][0]
    if colision(botones[3], posicion):
        respuesta = botones[3]["texto"][0]
    return respuesta

def formatear_texto(texto:str)->list:
    #evita que el texto se escape a la derecha si es muy largo
    lineas = texto.split(",")
    return lineas
 
def jugar(nombre_jugador:str)-> dict | None:
    pantalla = crear_superficie_pantalla()
    clock = pygame.time.Clock()
    fuente = crear_fuente(50)
    fondo = pygame.image.load("pyjuego/imagenes/castle2.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (1380,920 )) 

    # definir pregunta, opciones  y variantes
    pregunta_aleatoria = random.choice(list(preguntas.keys())) # cambiar por elegir_numero()
    pregunta_formateada = formatear_texto(preguntas[pregunta_aleatoria]["pregunta"])
    dibujar_pregunta(pregunta_formateada,400,50)
    dibujar_opciones(pantalla, preguntas ,pregunta_aleatoria)

    juego_terminado = False
    puntuacion = 0
    preguntas_correctas = 0
    sala = 1
    intentos = 2
    estado_final = False
    respuesta_final = ""
    resultados = crear_resultados(200,320,200,50)

    #definir botones
    boton_salir = crear_boton(480, 610, 250,80,"white", "Salir")
    botones = crear_botones_opciones(preguntas,pregunta_aleatoria)

    puntuacion_actual = fuente.render(f"puntaje: {puntuacion}", True, "black")
    intentos_actual = fuente.render(f"Intentos: {intentos}", True, "black")
    mensaje_final = fuente.render("Juego terminado", True, "black")
    cronometro = crear_cronometro(20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # al hacer click en la x de la ventana
                pygame.quit()
                sys.exit() # corta el programa 
            # hacer manejo de eventos de teclado
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #si el jugador abandona
                    if not juego_terminado: # previene que se guarde 2 veces al presionar en la pantalla de resultados
                        guardar_puntaje(nombre_jugador,estado_final,puntuacion)
                    running = False
                elif event.key == pygame.K_m:
                    entrar_sonido()
                    manejar_musica()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #hacer event casero
                if not juego_terminado:
                    respuesta_final  = manejo_click(botones,event.pos)
                else:
                    if colision(boton_salir, event.pos):
                        running = False

        pantalla.blit(fondo_escalado, (-50,-100))
        mx, my = pygame.mouse.get_pos()
        actualizar_tiempo(cronometro)
        
        if not juego_terminado:
            # --- pantalla de cuestionario ---
                dibujar_pregunta(pregunta_formateada,400,50)
                pantalla.blit(puntuacion_actual, (2, 400))
                pantalla.blit(intentos_actual,(2,100))
                dibujar_botones(botones,pantalla, (mx,my))
                dibujar_cronometro(cronometro,pantalla)
                
                if respuesta_final == preguntas[pregunta_aleatoria]["respuesta"]:
                    puntuacion += preguntas[pregunta_aleatoria]["valor_puntaje"]
                    preguntas_correctas += 1
                    respuesta_final = ""
                    respuesta_correcta()

                    puntaje_total = puntuacion
                    completar_resultados(resultados,sala,preguntas[pregunta_aleatoria]["valor_puntaje"],puntaje_total)
                    #poner el if else en una funcion
                    if preguntas_correctas >= 4 :
                        juego_terminado = True
                        estado_final = True
                        guardar_puntaje(nombre_jugador,estado_final,puntuacion)
                        
                    else:   
                        pregunta_aleatoria = random.choice(list(preguntas.keys())) # poner lambda
                        pregunta_formateada = formatear_texto(preguntas[pregunta_aleatoria]["pregunta"])
                        dibujar_pregunta(pregunta_formateada,400,50)
                        botones = crear_botones_opciones(preguntas, pregunta_aleatoria)
                        dibujar_botones(botones,pantalla, (mx,my))
                        intentos = 2
                        sala +=1
                        resetear_cronometro(cronometro)
                #poner en funcion
                elif respuesta_final != "" and respuesta_final != preguntas[pregunta_aleatoria]["respuesta"]:
                    intentos -= 1
                    respuesta_final = ""

                #poner en funcion
                if intentos < 1 or cronometro["tiempo_terminado"]:
                  juego_terminado = True
                  guardar_puntaje(nombre_jugador,estado_final,puntuacion)
                    
                puntuacion_actual = fuente.render(f"puntaje: {puntuacion}", True, "black")
                intentos_actual = fuente.render(f"Intentos: {intentos}", True, "black")  
                pantalla.blit(puntuacion_actual, (2, 400))
                pantalla.blit(intentos_actual,(2,100))

        else:
            pantalla.blit(mensaje_final, (480,50))
            resultado_jugador = dibujar_estado(nombre_jugador,estado_final)
            pantalla.blit(resultado_jugador[0], (500,100))
            pantalla.blit(resultado_jugador[1], (540,180))
            dibujar_resultados(resultados,pantalla)
            dibujar_botones(boton_salir, pantalla, (mx, my))
               
        pygame.display.flip()
        clock.tick(60)

    resultados_jugador = {"nombre": nombre_jugador, "puntuacion": puntuacion, "salas": sala, "gano": estado_final}
    return resultados_jugador

