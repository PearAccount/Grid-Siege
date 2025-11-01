import pygame
from ..settings import COLORS
from ..ui import Button

class VictoryScreen:
    def __init__(self, screen, on_menu):
        self.screen = screen
        self.on_menu = on_menu
        self.font_title = pygame.font.SysFont(None, 72)
        self.font_btn = pygame.font.SysFont(None, 36)
        self.title = self.font_title.render("You Win!", True, COLORS['ui'])

        w, h = self.screen.get_size()
        bw, bh = 280, 60
        self.btn_menu = Button((w//2 - bw//2, h//2 + 40, bw, bh), "Return to Menu", self.on_menu, self.font_btn)

    def handle_event(self, e):
        self.btn_menu.handle_event(e)

    def draw(self):
        # dimmed background
        veil = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 160))
        self.screen.blit(veil, (0, 0))

        w, h = self.screen.get_size()
        self.screen.blit(self.title, (w//2 - self.title.get_width()//2, h//2 - 60))
        self.btn_menu.draw(self.screen)
