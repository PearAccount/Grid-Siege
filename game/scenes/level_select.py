import pygame
from ..settings import COLORS
from ..ui import Button
class LevelSelectScreen:
    def __init__(self, screen, levels, on_choose_level, on_back):
        self.screen = screen
        self.levels = levels
        self.on_choose_level = on_choose_level
        self.on_back = on_back
        self.font_title = pygame.font.SysFont(None,56)
        self.font_btn = pygame.font.SysFont(None,32)
        self.title = self.font_title.render('Select Level', True, COLORS['ui'])
        w,h = self.screen.get_size()
        cols = 3
        gap = 18
        bw,bh = 280,56
        total_w = cols*bw+(cols-1)*gap; start_x = w//2-total_w//2; start_y = h//2-120
        self.buttons = []

        for i,lv in enumerate(self.levels):
            col = i%cols
            row = i//cols
            x = start_x+col*(bw+gap)
            y = start_y+row*(bh+gap)

            def make_cb(path = lv['path']):
                return lambda: self.on_choose_level(path)
            
            self.buttons.append(Button((x,y,bw,bh), lv['name'], make_cb(), self.font_btn))
        self.btn_back  =  Button((40, h-80, 160, 50), 'Back', self.on_back, self.font_btn)

    def handle_event(self,e):
        for b in self.buttons:
            b.handle_event(e)
        self.btn_back.handle_event(e)

    def draw(self):
        self.screen.fill((18,18,18))
        w,h = self.screen.get_size()
        self.screen.blit(self.title,(w//2-self.title.get_width()//2,100))
        for b in self.buttons:
            b.draw(self.screen)
        self.btn_back.draw(self.screen)
