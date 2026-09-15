import pygame

from objetos.Caja import *
from configuracion import *

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

def respuesta_correcta() -> None:
    #screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    #clock = pygame.time.Clock()

    # convert cuando no necesitas transparencia, convert_alpha cuando si
    boton_musica = Caja(1100, 620, 150,70, "white", "musica")
    boton_salir = Caja(450, 600, 300,80,"white", "continuar")
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
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
    boton_musica = Caja(1100, 620, 150,70, "white", "musica")
    boton_salir = Caja(400, 600, 450,100,"white", "Salir")

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