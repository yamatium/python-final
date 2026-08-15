import pygame
from configuracion import *

class Box:
    def __init__(self,x,y,w,h,color, texto="",draw_bg=True):
        self.color = color
        self.rect = pygame.Rect(x,y,w,h)
        self.texto = texto
        self.draw_bg = draw_bg

        #texto
        self.font = pygame.font.SysFont("Arial", 34)
        self.text_surf = self.font.render(self.texto, True, "black") 
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
    
    def draw(self,surface):
        if self.draw_bg:                         # <-- only draw rect if True
            pygame.draw.rect(surface, self.color, self.rect)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        surface.blit(self.text_surf, self.text_rect)

    def sonidoClick(self, estado="entrar"):
        self.estado = estado
        if self.estado == "entrar":
            entrar_sonido()
        else:
            salir_sonido()

#def dibujar_botones(botones, screen, mouse_pos):
#    for boton in botones:
#        boton.draw(screen)
#        boton.color = COLORS["lightblue"] if boton.collidepoint(mouse_pos) else COLORS["white"]
def dibujar_botones(botones, screen, mouse_pos):
    if type(botones) == list: # revisa que sea una lista
        for boton in botones:
            boton.draw(screen)
            boton.color = COLORS["lightblue"] if boton.collidepoint(mouse_pos) else COLORS["white"]
    else: 
        botones.draw(screen)
        botones.color = COLORS["lightblue"] if botones.collidepoint(mouse_pos) else COLORS["white"]