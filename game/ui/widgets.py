import pygame
class Button:
    def __init__(self, rect, text, on_click, font, padding=12):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.font = font
        self.padding = padding
        self.hover = False
        self.txt_surf = self.font.render(self.text, True, (20,20,20))
        tw, th = self.txt_surf.get_size()

        if self.rect.w < tw + self.padding*2: 
            self.rect.w = tw + self.padding*2
        if self.rect.h < th + self.padding*2: 
            self.rect.h = th + self.padding*2

    def handle_event(self, e):
        if e.type == pygame.MOUSEMOTION: 
            self.hover = self.rect.collidepoint(e.pos)  
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            if self.rect.collidepoint(e.pos): 
                self.on_click()

    def draw(self, surf):
        bg = (235,235,235) if not self.hover else (255,255,255)     # Change color when hovered
        pygame.draw.rect(surf, bg, self.rect, border_radius=10)
        pygame.draw.rect(surf, (60,60,60), self.rect, 2, border_radius=10)
        surf.blit(self.txt_surf, (self.rect.centerx - self.txt_surf.get_width()//2, self.rect.centery - self.txt_surf.get_height()//2))
