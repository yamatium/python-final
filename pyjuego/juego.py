import pygame
import random

from settings import *
from box import Box
from dibujar_Resultados import *
from ingresar_datos import *

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def jugar():
    color_active = (255, 255, 255)
    color_passive = (100, 100, 100)
    tabla_resultados = dibujar_Resultados(x=100, y=200, cell_w=150, cell_h=50)
    tabla_resultado_final = TablaResultadoFinal(x=100, y=100, cell_w=225, cell_h=50)

    nombre_jugador,b = ingreso_datos() # llama al ingreso de datos loop, regresa el nombre y continua al loop principal
    juego_terminado = False

    #posible uso de set
    #picked = set()
    #while len(picked) < 5:
    #    picked.add(random.randint(1, 20))
    #print(picked)  # {3, 7, 12, 15, 19} — no duplicates ✅

    # definir pregunta, opciones  y variantes
    pregunta_aleatoria = random.choice(list(preguntas.keys()))
    pregunta_actual = preguntas[pregunta_aleatoria]["pregunta"]
    opcion_a = preguntas[pregunta_aleatoria]["opciones"][0]
    opcion_b = preguntas[pregunta_aleatoria]["opciones"][1]
    opcion_c = preguntas[pregunta_aleatoria]["opciones"][2]
    opcion_d = preguntas[pregunta_aleatoria]["opciones"][3]
    puntuacion = 0
    preguntas_correctas = 0
    sala = 1
    intentos = 2
    estado_final = False
    texto_activo = False
    respuesta = ""
    respuesta_final = ""

    #definir rectangulos para usar con  variables
    rect_ingreso = pygame.Rect(500, 580, 180, 40)
    rect_responder = Box(500, 650, 200, 70, "white", "Continuar")
    block_a = Box(600,330,200,70,"white", f"{opcion_a}")
    block_b = Box(850,330,200,70, "white", f"{opcion_b}")
    block_c = Box(600,430,200,70,"white", f"{opcion_c}")
    block_d = Box(850,430,200,70,"white", f"{opcion_d}")
    block_pregunta = Box(600,30,450,200,"green", f"{pregunta_actual}")
    block_puntuacion = Box(210,350,200,80,"gray", f"puntaje: {puntuacion}" )
    block_correctas = Box(100,350,200,80, "gray", f"{preguntas_correctas}")
    block_salir = Box(600, 640, 450,100,"white", "Salir")
    block_final = Box(600, 50, 400, 100, "green", "Juego terminado!")

    click = False
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if texto_activo:
                    if event.key == pygame.K_BACKSPACE:
                        respuesta = respuesta[:-1]
                    else:
                        if len(respuesta) < 1 and validar_letra(event.unicode, "juego"):
                            respuesta += event.unicode
            # event.pos es una tupla de la posicion del mouse cuando el evento pasa (x,y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:# solo el click izquierdo del mouse
                    if not juego_terminado:
                        if rect_ingreso.collidepoint(event.pos):
                            texto_activo = True
                        else:
                            texto_activo = False
                        if rect_responder.collidepoint(event.pos):
                            respuesta_final = respuesta
                            respuesta = ""
                    else:
                        if block_salir.collidepoint(event.pos):
                            running = False


        screen.fill(COLORS["royalblue"])
        mx, my = pygame.mouse.get_pos()
        color_nombre = color_active if texto_activo else color_passive
        
        if not juego_terminado:
            # --- pantalla de cuestionario ---
                block_a.draw(screen)
                block_b.draw(screen)
                block_c.draw(screen)
                block_d.draw(screen)
                block_pregunta.draw(screen)
                block_puntuacion.draw(screen)
                block_correctas.draw(screen)
                rect_responder.draw(screen)
                pygame.draw.rect(screen, color_nombre, rect_ingreso)
                superficie_texto = font.render(respuesta, True, (0, 0, 0))
                screen.blit(superficie_texto, (rect_ingreso.x + 5, rect_ingreso.y + 5))
                

                #revisa que el mouse este en los rectangulos de opciones y cambia el color
                if rect_responder.collidepoint((mx,my)):
                    rect_responder.color = COLORS["lightblue"]
                else:
                    rect_responder.color = COLORS["white"]
                rect_responder.draw(screen)
                
                if respuesta_final == preguntas[pregunta_aleatoria]["respuesta"]:
                    puntuacion += preguntas[pregunta_aleatoria]["valor_puntaje"]
                    preguntas_correctas += 1
                    respuesta_final = ""

                    tabla_resultados.agregar_resultado(
                        nombre_sala=f"Sala {sala}",
                        puntaje_sala= preguntas[pregunta_aleatoria]["valor_puntaje"],
                        puntaje_total=puntuacion
                        )

                    if preguntas_correctas >= 4 :
                        juego_terminado = True
                        estado_final = True
                        tabla_resultado_final.agregar_resultado(nombre_jugador, estado_final)
                    else:   
                        pregunta_aleatoria = random.choice(list(preguntas.keys()))
                        pregunta_actual = preguntas[pregunta_aleatoria]["pregunta"]
                        opciones = preguntas[pregunta_aleatoria]["opciones"]
                        block_pregunta = Box(600, 30, 450, 200, "green", pregunta_actual)
                        block_a = Box(600, 330, 200, 70, "white", opciones[0])
                        block_b = Box(850, 330, 200, 70, "white", opciones[1])
                        block_c = Box(600, 430, 200, 70, "white", opciones[2])
                        block_d = Box(850, 430, 200, 70, "white", opciones[3])
                        opciones_blocks = [block_a, block_b, block_c, block_d]
                        pygame.draw.rect(screen, color_nombre, rect_ingreso)
                        screen.blit(superficie_texto, (rect_ingreso.x + 5, rect_ingreso.y + 5))
                        intentos = 2
                        sala +=1

                elif respuesta_final != "" and respuesta_final != preguntas[pregunta_aleatoria]["respuesta"]:
                    intentos -= 1
                    print(f"incorrecto intentos: {intentos}")
                    respuesta_final = ""

                if intentos < 1:
                    juego_terminado = True
                    estado_final = False
                    tabla_resultado_final.agregar_resultado(nombre_jugador, False)
                    
                
                block_puntuacion = Box(410, 350, 200, 80, "gray", f"puntaje: {puntuacion}")  # recreate with updated score
                block_puntuacion.draw(screen)
                block_correctas = Box(200,350,200,80, "gray", f"{preguntas_correctas}")
                block_correctas.draw(screen)
                

        else:
            block_final.draw(screen)
            tabla_resultados.draw(screen)
            tabla_resultado_final.draw(screen)
            block_salir.draw(screen)
            
        click = False
        pygame.display.flip()
        clock.tick(60)