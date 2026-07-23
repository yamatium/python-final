import pygame
from settings import *
from box import Box
import random
from settings import *

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def jugar():
    # input box setup
    font = pygame.font.SysFont(None, 50)
    user_text = ''
    active = False
    input_rect = pygame.Rect(500, 300, 200, 40)
    color_active = (255, 255, 255)
    color_passive = (100, 100, 100)

    # boxes for name input screen
    blockjuego = Box(450, 130, 300, 100, "white", "Ingresa tu nombre")
    blockcaja = Box(500, 550, 200, 70, "white", "Continuar")

    nombre_ingresado = False  # flag to switch from input screen to quiz screen
    juego_terminado = False

    # definir pregunta y las opciones
    pregunta_aleatoria = random.choice(list(preguntas.keys()))
    pregunta_actual = preguntas[pregunta_aleatoria]["pregunta"]
    opcion_a = preguntas[pregunta_aleatoria]["opciones"][0]
    opcion_b = preguntas[pregunta_aleatoria]["opciones"][1]
    opcion_c = preguntas[pregunta_aleatoria]["opciones"][2]
    opcion_d = preguntas[pregunta_aleatoria]["opciones"][3]
    puntuacion = 0
    preguntas_correctas = 0
    #definir rectangulos y usar variables
    block_a = Box(600,530,200,70,"white", f"{opcion_a}")
    block_b = Box(850,530,200,70, "white", f"{opcion_b}")
    block_c = Box(600,630,200,70,"white", f"{opcion_c}")
    block_d = Box(850,630,200,70,"white", f"{opcion_d}")
    block_pregunta = Box(600,30,450,200,"green", f"{pregunta_actual}")
    block_puntuacion = Box(710,350,200,80,"gray", f"puntaje: {puntuacion}" )
    block_correctas = Box(500,350,200,80, "gray", f"{preguntas_correctas}")
    block_final = Box(600, 200, 450, 100, "green", f"Juego terminado!")
    block_salir = Box(600, 640, 450,100,"white", "Salir")

    opciones_blocks = [block_a, block_b, block_c, block_d]

    respuesta = ""
    click = False
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if active and not nombre_ingresado:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        if len(user_text) < 10:
                            user_text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:# solo el click izquierdo del mouse
                    click = True
                    if not nombre_ingresado:
                        if input_rect.collidepoint(event.pos):
                            active = True
                        else:
                            active = False
                        # continue button — only if name has been typed
                        if blockcaja.collidepoint(event.pos) and len(user_text) > 0:
                            nombre_ingresado = True  # switch to quiz screen

        screen.fill(COLORS["royalblue"])
        mx, my = pygame.mouse.get_pos()

        if not nombre_ingresado:
            # --- ingresar nombre pantalla ---
            blockjuego.draw(screen)
            blockcaja.draw(screen)
            color = color_active if active else color_passive
            pygame.draw.rect(screen, color, input_rect)
            text_surface = font.render(user_text, True, (0, 0, 0))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
            input_rect.w = text_surface.get_width() + 10

        elif not juego_terminado:
            # --- cuestionario ---
                block_a.draw(screen)
                block_b.draw(screen)
                block_c.draw(screen)
                block_d.draw(screen)
                block_pregunta.draw(screen)
                block_puntuacion.draw(screen)
                block_correctas.draw(screen)

                #revisa que el mouse este en los rectangulos de opciones
                for block in opciones_blocks:
                    if block.collidepoint((mx, my)):
                        if click:
                            respuesta = block.texto[0]
                            print(block.texto[0])
                
                if respuesta == preguntas[pregunta_aleatoria]["respuesta"]:
                    puntuacion += preguntas[pregunta_aleatoria]["valor_puntaje"]
                    preguntas_correctas += 1
                    print(puntuacion)

                    if preguntas_correctas >= 4:
                        juego_terminado = True
                        block_score = Box(600, 320, 450, 100, "white", f"Puntaje final: {puntuacion}")
                        block_nombre = Box(600, 440, 450, 100, "white", f"Jugador: {user_text}")
                    else:   
                        pregunta_aleatoria = random.choice(list(preguntas.keys()))
                        pregunta_actual = preguntas[pregunta_aleatoria]["pregunta"]
                        opciones = preguntas[pregunta_aleatoria]["opciones"]
                        block_pregunta = Box(600, 30, 450, 200, "green", pregunta_actual)
                        block_a = Box(600, 530, 200, 70, "white", opciones[0])
                        block_b = Box(850, 530, 200, 70, "white", opciones[1])
                        block_c = Box(600, 630, 200, 70, "white", opciones[2])
                        block_d = Box(850, 630, 200, 70, "white", opciones[3])
                        opciones_blocks = [block_a, block_b, block_c, block_d]
    
                block_puntuacion = Box(710, 350, 200, 80, "gray", f"puntaje: {puntuacion}")  # recreate with updated score
                block_puntuacion.draw(screen)
                block_correctas = Box(500,350,200,80, "gray", f"{preguntas_correctas}")
                block_correctas.draw(screen)
                respuesta = ""

        else:
            #block_final = Box(600, 200, 450, 100, "green", f"Juego terminado!")
            #block_score = Box(600, 320, 450, 100, "white", f"Puntaje final: {puntuacion}")
            #block_nombre = Box(600, 440, 450, 100, "white", f"Jugador: {user_text}")
            #block_salir = Box(600, 640, 450,100,"white", "Salir")
            block_final.draw(screen)
            block_score.draw(screen)
            block_nombre.draw(screen)
            block_salir.draw(screen)
            if block_salir.collidepoint((mx, my)):
                if click:
                    running = False
            
        click = False
        pygame.display.flip()
        clock.tick(60)