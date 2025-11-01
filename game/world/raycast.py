from .grid import grid_at

def raycast(grid, start, end, hit_soft_as_block=True):
    x0, y0 = start
    x1, y1 = end
    dx, dy = x1-x0, y1-y0
    steps = int(max(abs(dx), abs(dy)) // 4) + 1
    for i in range(steps+1):
        t = i / steps; x = x0 + dx * t; y = y0 + dy * t
        ch = grid_at(grid,x,y)
        if ch == '#': 
            return True, (x,y),'#'
        if ch == 's' and hit_soft_as_block: 
            return True, (x,y),'s'
    return False, end, '.'
