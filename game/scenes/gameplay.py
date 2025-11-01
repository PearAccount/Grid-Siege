import pygame
from ..settings import WIDTH, HEIGHT, COLORS, CROSSHAIR_PULSE_ON_SHOT, SHAKE_ON_SHOT
from ..world import map_from_file, find_positions, get_camera_offset, draw_grid
from ..entities import Player, Enemy
from ..utils import add_shake, update_shake, add_crosshair_pulse, update_crosshair_pulse
class GameScene:
    def __init__(self, screen, font, level_path):
        self.screen = screen
        self.font = font
        self.level_path = level_path
        self.grid = None
        self.player = None
        self.enemies = []
        self.bullets = []

    def load_level(self, level_path = None):
        if level_path is not None: 
            self.level_path = level_path

        grid = map_from_file(self.level_path)
        ppos, es = find_positions(grid)
        self.grid = grid
        self.player = Player(ppos if ppos else (64,64))
        self.enemies = [Enemy(e['pos']) for e in es]
        self.bullets.clear()

    def step(self, dt, events):     # The updating function when playing
        keys = pygame.key.get_pressed()
        self.player.update(dt,self.grid,keys)
        base_cam = get_camera_offset(self.grid,self.player.x,self.player.y)
        shake_off = update_shake(dt)
        cam = (base_cam[0]+shake_off[0], base_cam[1]+shake_off[1])
        self.bullets = [b for b in self.bullets if b.update(dt,self.grid,self.player,[vars(e) for e in self.enemies])]

        for en in self.enemies: 
            en.update(dt,self.grid,self.player,self.bullets,self.enemies)
        if not self.player.alive: 
            self.load_level()

        if self.player.alive and all(not en.alive for en in self.enemies):
            return "victory"

        #cam = get_camera_offset(self.grid,self.player.x,self.player.y)  Make the cam back to default
        self.screen.fill(COLORS['bg'])
        draw_grid(self.screen,self.grid,cam)

        for b in self.bullets: 
            b.draw(self.screen,cam)
        for en in self.enemies: 
            en.draw(self.screen,cam)

        mouse_world = (pygame.mouse.get_pos()[0]+base_cam[0], pygame.mouse.get_pos()[1]+base_cam[1])
        self.player.draw(self.screen,cam,mouse_world)
        crosshair_scale = 1.0+update_crosshair_pulse(dt)
        self.draw_crosshair(self.screen, pygame.mouse.get_pos(), crosshair_scale)
        info = self.font.render('LMB shoot | RMB melee | R restart | ESC pause', True, COLORS['ui'])
        self.screen.blit(info,(10,HEIGHT-26))

        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    base_cx,base_cy = base_cam
                    mw = (pygame.mouse.get_pos()[0]+base_cx, pygame.mouse.get_pos()[1]+base_cy)
                    self.player.shoot(mw, self.bullets)
                    add_shake(SHAKE_ON_SHOT)
                    add_crosshair_pulse(CROSSHAIR_PULSE_ON_SHOT)

                elif e.button == 3:
                    base_cx,base_cy = base_cam
                    mw = (pygame.mouse.get_pos()[0]+base_cx, pygame.mouse.get_pos()[1]+base_cy)
                    from ..world.raycast import raycast
                    self.player.melee(mw, self.grid, raycast)

            elif e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                self.load_level()

    def draw_crosshair(self, surf, screen_pos, scale: float  =  1.0):
        x,y = screen_pos
        r = int(8*scale)
        arm_inner = int(3*scale)
        arm_outer = int(10*scale)
        thick = 2

        pygame.draw.circle(surf, COLORS['ui'], (int(x),int(y)), r, thick)
        pygame.draw.line(surf, COLORS['ui'], (x-arm_outer,y), (x-arm_inner,y), thick)
        pygame.draw.line(surf, COLORS['ui'], (x+arm_inner,y), (x+arm_outer,y), thick)
        pygame.draw.line(surf, COLORS['ui'], (x,y-arm_outer), (x,y-arm_inner), thick)
        pygame.draw.line(surf, COLORS['ui'], (x,y+arm_inner), (x,y+arm_outer), thick)
