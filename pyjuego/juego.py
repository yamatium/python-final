import pygame
import random

from puntuacion import *
from configuracion import *
from objetos.box import Box
from objetos.dibujar_Resultados import *
from objetos.temporizador import *

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def dibujar_opciones(screen, pregunta_aleatoria) -> None:
    opciones = preguntas[pregunta_aleatoria]["opciones"]
    posiciones = [(350, 330), (620, 330), (350, 430), (620, 430)]

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

def jugar():
    color_active = (255, 255, 255)
    color_passive = (100, 100, 100)
    tabla_resultados = dibujar_Resultados(200,320,200,50)
    #custom = pygame.font.SysFont(None, 50)
    #imagenes
    fondo = pygame.image.load("pyjuego/imagenes/castle2.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (WINDOW_WIDTH + 100, WINDOW_HEIGHT +200 ))

    nombre_jugador = ingreso_datos() # llama al ingreso de datos loop, regresa el nombre y continua al loop principal
    if nombre_jugador is None:
        return None
    juego_terminado = False

    # definir pregunta, opciones  y variantes
    pregunta_aleatoria = random.choice(list(preguntas.keys()))
    pregunta_actual2 = font.render(f"{preguntas[pregunta_aleatoria]["pregunta"]}", True, "black")
    screen.blit(pregunta_actual2, (400, 50))
    dibujar_opciones(screen, pregunta_aleatoria)

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
    rect_responder = Box(500, 630, 200, 70, "white", "Continuar")
    boton_salir = Box(480, 610, 250,80,"white", "Salir")
    puntuacion_actual = font.render(f"puntaje: {puntuacion}", True, "black")
    mensaje_final = font.render("Juego terminado", True, "black")

    tiempo = Temporizador(20)
    juego_pausa = False
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    juego_pausa = True
                    print("pausa")
                if event.key == pygame.K_m:
                    entrar_sonido()
                    manejar_musica()
                if texto_activo:
                    if event.key == pygame.K_BACKSPACE:
                        respuesta = respuesta[:-1]
                    else:
                        if len(respuesta) < 1 and validar_letra(event.unicode, "juego"):
                            respuesta += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not juego_terminado:
                        if rect_ingreso.collidepoint(event.pos):
                            texto_activo = True
                        else:
                            texto_activo = False
                        if rect_responder.collidepoint(event.pos):
                            respuesta_final = respuesta
                            respuesta = ""
                    else:
                        if boton_salir.collidepoint(event.pos):
                            running = False

        screen.blit(fondo_escalado, (-50,-100))
        mx, my = pygame.mouse.get_pos()
        color_nombre = color_active if texto_activo else color_passive
        tiempo.update()
        
        if not juego_terminado:
            # --- pantalla de cuestionario ---

                screen.blit(pregunta_actual2, (400,50))
                dibujar_opciones(screen, pregunta_aleatoria)
                screen.blit(puntuacion_actual, (2, 400))
                #block_correctas.draw(screen)
                tiempo.draw(screen)

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
                        pregunta_actual2 = font.render(f"{preguntas[pregunta_aleatoria]["pregunta"]}", True, "black")
                        screen.blit(pregunta_actual2, (400, 50))
                        dibujar_opciones(screen, pregunta_aleatoria)
                        screen.blit(pregunta_actual2, (400,50))
                        pygame.draw.rect(screen, color_nombre, rect_ingreso)
                        screen.blit(superficie_texto, (rect_ingreso.x + 5, rect_ingreso.y + 5))
                        intentos = 2
                        sala +=1
                        tiempo.reset()

                elif respuesta_final != "" and respuesta_final != preguntas[pregunta_aleatoria]["respuesta"]:
                    intentos -= 1
                    print(f"incorrecto intentos: {intentos}")
                    respuesta_final = ""

                if intentos < 1 or tiempo.terminado:
                    juego_terminado = True
                    estado_final = False
                    guardar_puntaje(nombre_jugador,estado_final,puntuacion)
                    
                puntuacion_actual = font.render(f"puntaje: {puntuacion}", True, "black")   # recreate with updated score
                screen.blit(puntuacion_actual, (2, 400))
                

        else:
            screen.blit(mensaje_final, (480,50))
            resultado_jugador = dibujar_estado(nombre_jugador,estado_final)
            screen.blit(resultado_jugador[0], (500,100))
            screen.blit(resultado_jugador[1], (540,180))
            tabla_resultados.draw(screen,font)
            dibujar_botones(boton_salir, screen, (mx, my))
            
        pygame.display.flip()
        clock.tick(60)

    resultados = {"nombre": nombre_jugador, "puntuacion": puntuacion, "salas": sala, "gano": estado_final}
    return resultados

def respuesta_correcta() -> None:
    clock = pygame.time.Clock()

    # convert cuando no necesitas transparencia, convert_alpha cuando si
    boton_musica = Box(1100, 620, 150,70, "white", "musica")
    boton_salir = Box(450, 600, 300,80,"white", "continuar")
    botones = [boton_musica,boton_salir]
    bien = pygame.image.load("pyjuego/imagenes/thumbs-up.png").convert()
    bien_scale = pygame.transform.scale(bien, (498,390))

    fondo_puerta = pygame.image.load("pyjuego/imagenes/doorTrans.png").convert_alpha()
    fondo_real = pygame.image.load("pyjuego/imagenes/campo2.png").convert()
    fondo_scale = pygame.transform.scale(fondo_puerta, (1500,700))

    puerta_izquierda = pygame.image.load("pyjuego/imagenes/door2.png").convert_alpha()
    izquierda_scale = pygame.transform.scale(puerta_izquierda, (300,450))
    puerta_derecha = pygame.image.load("pyjuego/imagenes/door1.png").convert_alpha()
    derecha_scale = pygame.transform.scale(puerta_derecha, (300,450))

    mensaje = font.render("Respuesta Correcta!", True, "black")

    x = 305
    z = 600
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if boton_salir.collidepoint(event.pos):
                        running = False
                    if boton_musica.collidepoint(event.pos):
                        entrar_sonido()
                        manejar_musica()

        mx, my = pygame.mouse.get_pos()
        screen.blit(fondo_real, (0,0))
        screen.blit(bien_scale, (340,160))
        screen.blit(mensaje, (410,120))
        screen.blit(fondo_scale, (-100, -120))
        screen.blit(izquierda_scale, (x,100))
        screen.blit(derecha_scale, (z,100))

        dibujar_botones(botones,screen,(mx,my))
        x -= 0.6
        z += 0.6
        
        pygame.display.flip()
        clock.tick(60)



def mostrar_torneo(resultados) -> None:

    fondo = pygame.image.load("pyjuego/imagenes/forest.png").convert()
    fondo_escalado = pygame.transform.scale(fondo, (WINDOW_WIDTH + 100, WINDOW_HEIGHT +200 ))
    boton_musica = Box(1100, 620, 150,70, "white", "musica")
    boton_salir = Box(400, 600, 450,100,"white", "Salir")

    botones = [boton_musica,boton_salir]
    # 1. mayor puntaje
    max_puntaje = max(r["puntuacion"] for r in resultados)
    ganadores_puntaje = [r["nombre"] for r in resultados if r["puntuacion"] == max_puntaje]
    # 2. quien llego mas lejos (mas salas)
    max_salas = max(r["salas"] for r in resultados)
    ganadores_salas = [r["nombre"] for r in resultados if r["salas"] == max_salas]
    # 3. no superaron sala 1
    eliminados_sala = [r["nombre"] for r in resultados if r["salas"] == 1 and not r["gano"]]
    #https://www.pygame.org/docs/ref/color_list.html
    titulo = font.render("Resultados del Torneo", True, "white")
    puntaje = font.render(f"Mayor puntaje ({max_puntaje} pts): {', '.join(ganadores_puntaje)}", True, "yellow")
    sala = font.render(f"Llegaron mas lejos (sala {max_salas}): {', '.join(ganadores_salas)}", True, "aqua")

    # --- pantalla de resultados ---
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
                    if boton_salir.collidepoint(event.pos):
                        running = False
                if boton_musica.collidepoint(event.pos):
                        entrar_sonido()
                        manejar_musica()

        if eliminados_sala:
            texto = font.render(f"No superaron sala 1: {', '.join(eliminados_sala)}", True, "red")
        else:
            texto = font.render("Todos superaron la sala 1!", True, "green")

        screen.blit(fondo_escalado, (-50,-100))
        mx, my = pygame.mouse.get_pos()
        dibujar = [titulo,puntaje,sala,texto]
        posiciones = [(400, 40),(400, 240),(400, 290),(400, 340)]  
        for i in range(4):
            screen.blit(dibujar[i], (posiciones[i]))
        dibujar_botones(botones,screen,(mx,my))
        pygame.display.flip()
        clock.tick(60)