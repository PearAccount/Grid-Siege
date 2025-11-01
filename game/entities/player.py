import pygame
from ..utils.math2d import v_sub, v_norm, v_len
from ..world.grid import rect_free
from ..settings import PLAYER_SPEED, FIRE_COOLDOWN, BULLET_SPEED, MELEE_RANGE, COLORS
from .bullet import Bullet
class Player:
    def __init__(self,pos): 
        self.x,self.y = pos
        self.radius = 12; self.cooldown = 0.0
        self.alive = True

    def update(self,dt,grid,keys):
        if not self.alive: 
            return
        
        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]
        mag = (dx*dx+dy*dy)**0.5

        if mag: 
            dx /= mag; dy /= mag
            
        vx, vy = dx*PLAYER_SPEED, dy*PLAYER_SPEED
        rect = pygame.Rect(0,0,self.radius*2,self.radius*2)
        rect.center = (self.x+vx*dt,self.y)
        if rect_free(grid,rect): 
            self.x += vx*dt
        rect.center = (self.x,self.y+vy*dt)
        if rect_free(grid,rect): 
            self.y += vy*dt
        self.cooldown = max(0.0,self.cooldown-dt)
    def shoot(self,target_world,bullets):
        if not self.alive or self.cooldown>0: 
            return
        
        d = v_sub(target_world,(self.x,self.y))
        d = v_norm(d)

        bullets.append(Bullet((self.x,self.y),(d[0]*BULLET_SPEED,d[1]*BULLET_SPEED)))
        self.cooldown = FIRE_COOLDOWN

    def melee(self,target_world,grid,raycast_fn):
        if not self.alive: 
            return
        d = v_sub(target_world,(self.x,self.y))
        dist = v_len(d)
        if dist == 0:
            return
        d = (d[0]/dist,d[1]/dist)
        reach = min(MELEE_RANGE,dist)
        end = (self.x+d[0]*reach,self.y+d[1]*reach)
        hit, hp, tile = raycast_fn(grid,(self.x,self.y),end,True)
        if hit and tile == 's':
            from ..world.grid import set_grid; set_grid(grid,hp[0],hp[1],'.')

    def draw(self,surf,cam,aim_world):
        cx,cy = cam
        pygame.draw.circle(surf,COLORS['player'],(int(self.x-cx),int(self.y-cy)),self.radius)
        d = v_norm(v_sub(aim_world,(self.x,self.y)))
        tip = (self.x+d[0]*self.radius*1.2 - cx, self.y+d[1]*self.radius*1.2 - cy)
        pygame.draw.line(surf, COLORS['ui'], (self.x-cx,self.y-cy), tip, 2)
