import pygame
from ..settings import TILE, WIDTH, HEIGHT, COLORS

def map_from_file(path):    # Return level list
    with open(path, 'r', encoding='utf-8') as f:
        rows = [list(line.rstrip('\n')) for line in f if line.strip()]
    w = max(len(r) for r in rows)
    for r in rows:
        if len(r) < w:
            r.extend('#' for _ in range(w - len(r)))
    return rows

def find_positions(grid):   # Return entities' positions   
    p, enemies = None, []
    for r,row in enumerate(grid):
        for c,ch in enumerate(row):
            if ch=='P': p=(c*TILE+TILE/2,r*TILE+TILE/2); grid[r][c]='.'
            elif ch=='E': enemies.append({'pos':(c*TILE+TILE/2,r*TILE+TILE/2)}); grid[r][c]='.'
    return p,enemies

def in_world(grid, x, y): 
    return 0 <= x < len(grid[0])*TILE and 0 <= y < len(grid)*TILE

def grid_at(grid,x,y):  # Looks up tile's type at a specific world coordinate
    if not in_world(grid, x, y): return '#'
    c=int(x//TILE); r=int(y//TILE); return grid[r][c]

def set_grid(grid,x,y,ch):
    c=int(x//TILE); r=int(y//TILE)
    if 0<=r<len(grid) and 0<=c<len(grid[0]): grid[r][c]=ch

def rect_free(grid,rect):   # Collision check
    for x in (rect.left,rect.right-1):
        for y in (rect.top,rect.bottom-1):
            ch = grid_at(grid, x, y)
            if ch in ('#','s'): 
                return False
    return True

def clamp(v, lo, hi): 
    return max(lo, min(hi, v))

def get_camera_offset(grid, target_x, target_y):
    world_w = len(grid[0]) * TILE
    world_h = len(grid) * TILE
    max_x = max(0, world_w - WIDTH)
    max_y = max(0, world_h - HEIGHT)
    cam_x = clamp(target_x - WIDTH/2, 0, max_x)
    cam_y = clamp(target_y - HEIGHT/2, 0, max_y)
    return cam_x, cam_y

def draw_grid(surf,grid,cam):
    cx,cy=cam
    c0 = max(0, int(cx // TILE) - 1)
    r0 = max(0, int(cy // TILE) - 1)
    c1 = min(len(grid[0]), int((cx + surf.get_width()) // TILE) + 2)
    r1 = min(len(grid),   int((cy + surf.get_height()) // TILE) + 2)
    for r in range(r0, r1):
        for c in range(c0, c1):
            ch = grid[r][c]
            x = c*TILE - cx
            y = r*TILE - cy
            if ch=='#': 
                pygame.draw.rect(surf,COLORS['wall'],(x,y,TILE-1,TILE-1))
            elif ch=='s': 
                pygame.draw.rect(surf,COLORS['soft'],(x,y,TILE-1,TILE-1))
            else: 
                pygame.draw.rect(surf,COLORS['floor'],(x,y,TILE-1,TILE-1))
