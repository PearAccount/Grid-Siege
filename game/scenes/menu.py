import pygame
from ..settings import COLORS
from ..ui import Button
class MenuScreen:
    def __init__(self, screen, go_to_level_select, quit_game):
        self.screen = screen
        self.font_title = pygame.font.SysFont(None,72)
        self.font_btn = pygame.font.SysFont(None,36)
        self.title = self.font_title.render('Grid Siege', True, COLORS['ui'])
        w,h = self.screen.get_size()
        bw,bh = 280,60

        self.buttons = [
            Button((w//2-bw//2,h//2-10,bw,bh),'Play',go_to_level_select,self.font_btn),
            Button((w//2-bw//2,h//2+70,bw,bh),'Quit',quit_game,self.font_btn)
        ]

    def handle_event(self,e):
        for b in self.buttons: b.handle_event(e)
        
    def draw(self):
        self.screen.fill((18,18,18))
        w,h=self.screen.get_size()
        self.screen.blit(self.title,(w//2-self.title.get_width()//2,h//3-80))
        for b in self.buttons: b.draw(self.screen)
