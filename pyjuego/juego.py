import pygame
from settings import *
from box import Box

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
user_text = ''
cuadro_posicion = (WINDOW_WIDTH / 2 , WINDOW_HEIGHT /2 )
input_rect = pygame.Rect(200,200,140,32)
color_active = COLORS["lightblue"]
color_pasive = COLORS["gray"]
color = color_pasive

active = False

running = True

def jugar():
    blockjuego = Box(450,330,200,70,"white", "Jugar2")
    running = True
    active = False
    font = pygame.font.SysFont(None, 30)
    user_text = ''
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active == True:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
            

        screen.fill(COLORS["royalblue"])
        if active:
            color = color_active
        else:
            color = color_pasive
        pygame.draw.rect(screen,color,input_rect)
        blockjuego.draw(screen)
        text_surface = font.render(user_text,True,(255,255,255))
        screen.blit(text_surface,(input_rect.x + 5, input_rect.y + 5))

        input_rect.w = text_surface.get_width() + 10

        pygame.display.flip()
        clock.tick(60) 

