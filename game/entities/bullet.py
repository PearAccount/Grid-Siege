import pygame
from ..settings import BULLET_LIFETIME, COLORS
from ..world.grid import in_world, grid_at, set_grid

TRAIL_MAX_AGE = 0.25
TRAIL_MAX_POINTS = 14
TRAIL_MAX_WIDTH=6

class Bullet:
    def __init__(self, pos, vel, from_enemy=False):
        self.x, self.y=pos
        self.vx,self.vy = vel
        self.t = 0.0
        self.from_enemy = from_enemy
        self.trail=[(self.x,self.y,self.t)]

    def update(self, dt, grid, player, enemies):
        self.t += dt
        if self.t > BULLET_LIFETIME: 
            return False
            
        for _ in range(6):  # Move bullet 6 times per frame, smoother, prevent tunneling
            self.x += self.vx * dt / 6
            self.y += self.vy * dt / 6

            self.trail.append((self.x, self.y, self.t))
            if len(self.trail) > TRAIL_MAX_POINTS: 
                self.trail.pop(0)

            if not in_world(grid, self.x, self.y): 
                return False
            
            block = grid_at(grid, self.x, self.y)
            if block == '#': 
                return False
            if block == 's':    # Destroy soft walls
                set_grid(grid, self.x, self.y, '.')
                return False
            
            if self.from_enemy:
                if (self.x - player.x)**2 + (self.y - player.y)**2 <= player.radius**2:
                    player.alive = False
                    return False
            else:
                for e in enemies:
                    if not e['alive']:
                        continue
                    if (self.x - e['x'])**2 + (self.y - e['y'])**2 <= e['radius']**2:
                        e['alive'] = False
                        return False
                    
        cutoff = self.t - TRAIL_MAX_AGE      
        while self.trail and self.trail[0][2] < cutoff: # Remove the trail point that is too "old"
            self.trail.pop(0)
        return True
    
    def draw_trail(self, surf, cam):
        if len(self.trail) < 2: 
            return
        
        cx, cy = cam
        tsurf = pygame.Surface((surf.get_width(), surf.get_height()), pygame.SRCALPHA)

        def clamp(v, lo=0.0, hi=1.0): 
            return lo if v < lo else hi if v > hi else v
        
        for i in range(1, len(self.trail)):
            x1, y1, t1 = self.trail[i-1]
            x2, y2, t2 = self.trail[i]
            age = self.t - t2
            fade = clamp(1.0 - age / TRAIL_MAX_AGE)
            if fade <= 0: continue
            width = max(1, int(TRAIL_MAX_WIDTH * fade))
            col = (*COLORS['bullet'], int(255 * fade))
            pygame.draw.line(tsurf, col, (x1 - cx, y1 - cy), (x2 - cx, y2 - cy), width)
        surf.blit(tsurf, (0, 0))
        
    def draw(self, surf, cam):
        self.draw_trail(surf, cam)
        cx, cy = cam
        pygame.draw.circle(surf, COLORS['bullet'], (int(self.x - cx), int(self.y - cy)), 3)
