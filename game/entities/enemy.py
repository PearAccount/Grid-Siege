import random, pygame
from ..utils.math2d import v_norm, v_len
from ..world.grid import rect_free
from ..world.raycast import raycast
from ..world.pathfinding import astar, cell_from_world
from ..settings import ENEMY_VIEW_DIST, ENEMY_SPEED, BULLET_SPEED, ENEMY_FIRE_COOLDOWN, ALERT_RADIUS, ALERT_DURATION, COLORS
from .bullet import Bullet

class Enemy:
    def __init__(self,pos): 
        self.x,self.y=pos; self.radius=12; self.cooldown=random.uniform(0.1,0.4)
        self.alive=True
        self.wander_dir=v_norm((random.uniform(-1,1),random.uniform(-1,1)))
        self.wander_t=random.uniform(0.6,1.4)
        self.alert = 0.0
        self.path = []
        self._repath_timer = 0.0
        self._last_goal_cell = None
        self._last_known_player = pos

    def update(self, dt, grid, player, bullets, enemies):
        if not self.alive: 
            return
        
        to_player = (player.x - self.x, player.y - self.y)
        dist = v_len(to_player); sees = False
        if player.alive and dist < ENEMY_VIEW_DIST:
            hit, hp, tile = raycast(grid, (self.x, self.y), (player.x, player.y), True)
            if not hit: 
                sees = True

        if self.alert > 0.0:
            self.alert = max(0.0, self.alert - dt)
            sees = True

        if sees:
            self.alert = max(self.alert, ALERT_DURATION)
            for other in enemies:
                if other is self or not other.alive: 
                    continue
                dx = other.x - self.x 
                dy = other.y - self.y
                if dx*dx + dy*dy <= ALERT_RADIUS * ALERT_RADIUS:
                    hit, hp, tile = raycast(grid, (self.x, self.y), (other.x, other.y), True)
                    if not hit: 
                        other.alert = max(other.alert, ALERT_DURATION)
        chase = None
        if sees:
            self._last_known_player = (player.x, player.y)
            chase = self._last_known_player
        elif self.alert > 0.0:
            chase = self._last_known_player
        vx = vy = 0.0

        if chase:
            hit, _, _ = raycast(grid, (self.x, self.y), chase, True)
            if not hit:
                dirv = v_norm((chase[0] - self.x, chase[1] - self.y))
                vx, vy = dirv[0] * ENEMY_SPEED, dirv[1] * ENEMY_SPEED
                self.path.clear()
            else:
                self._repath_timer -= dt
                my_cell = cell_from_world(self.x, self.y)
                goal_cell = cell_from_world(*chase)
                need_repath = (not self.path) or (self._repath_timer<=0.0) or (self._last_goal_cell!=goal_cell)
                if need_repath:
                    self.path = astar(grid, my_cell, goal_cell); self._last_goal_cell = goal_cell; self._repath_timer = 0.25
                if self.path:
                    wp = self.path[0]
                    if v_len((wp[0] - self.x, wp[1] - self.y)) < 6.0:
                        self.path.pop(0)
                        if self.path: 
                            wp = self.path[0]
                    if self.path:
                        dirv = v_norm((wp[0] - self.x, wp[1] - self.y))
                        vx, vy = dirv[0] * ENEMY_SPEED, dirv[1] * ENEMY_SPEED
                else:
                    self.wander_t = min(self.wander_t, 0.1)
        else:
            self.wander_t -= dt
            if self.wander_t <= 0:
                self.wander_dir = v_norm((random.uniform(-1, 1), random.uniform(-1, 1)))
                self.wander_t = random.uniform(0.6, 1.6)
            vx = self.wander_dir[0] * ENEMY_SPEED * 0.5; vy = self.wander_dir[1] * ENEMY_SPEED * 0.5

        rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        rect.center = (self.x + vx * dt, self.y)

        if rect_free(grid, rect): 
            self.x += vx * dt
        else:
            if self.path: self._repath_timer = 0.0
        rect.center = (self.x, self.y + vy * dt)

        if rect_free(grid, rect): 
            self.y += vy * dt
        else:
            if self.path: self._repath_timer = 0.0

        self.cooldown = max(0.0, self.cooldown - dt)
        if sees and self.cooldown == 0.0 and player.alive:
            d = v_norm(to_player)
            bullets.append(Bullet((self.x, self.y), (d[0] * BULLET_SPEED * 0.8, d[1] * BULLET_SPEED * 0.8), True))
            self.cooldown = ENEMY_FIRE_COOLDOWN
        if player.alive and (self.x - player.x) ** 2 + (self.y - player.y) ** 2 <= (self.radius + player.radius) ** 2:
            player.alive = False
            
    def draw(self,surf,cam):
        if not self.alive: return
        cx,cy=cam
        pygame.draw.circle(surf, COLORS['enemy'], (int(self.x-cx), int(self.y-cy)), self.radius)
