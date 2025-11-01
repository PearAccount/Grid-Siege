import pygame
WIDTH, HEIGHT = 1600, 960
TILE = 32
FPS = 120
PLAYER_SPEED = 520
BULLET_SPEED = 3000
BULLET_LIFETIME = 0.8
FIRE_COOLDOWN = 0.15
MELEE_RANGE = 54
ENEMY_SPEED = 340
ENEMY_FIRE_COOLDOWN = 0.2
ENEMY_VIEW_DIST = 600
ALERT_RADIUS = 480
ALERT_DURATION = 3.0
COLORS = {'bg': (18,18,18),'floor':(35,35,40),'wall':(120,120,130),'soft':(165,120,85),'player':(90,200,255),'enemy':(255,95,95),'bullet':(255,255,255),'ui':(220,220,220)}
SHAKE_ON_SHOT = 12.0
SHAKE_DECAY = 500.0
CROSSHAIR_PULSE_ON_SHOT = 0.35
CROSSHAIR_PULSE_DECAY = 5.0
LEVELS = [
    {'name':'Training','path':'assets/levels/level_1.txt'},
    {'name':'Office','path':'assets/levels/level_2.txt'},
    {'name':'Mall','path':'assets/levels/level_3.txt'},
]
