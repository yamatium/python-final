import pygame

class Box:
    def __init__(self,x,y,w,h,color, texto=""):
        self.color = color
        self.rect = pygame.Rect(x,y,w,h)
        self.texto = texto

        #texto
        self.font = pygame.font.SysFont("Arial", 24)
        self.text_surf = self.font.render(texto, True, "red")
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)
    
    def draw(self,surface):
        #pygame.draw.rect(surface, self.color ,self.rect)
        #surface.blit(self.text_surf, self.text_rect)
        pygame.draw.rect(surface, self.color, self.rect)
        self.text_surf = self.font.render(self.texto, True, "red")  # re-render every frame
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        surface.blit(self.text_surf, self.text_rect)

