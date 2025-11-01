import heapq
from ..settings import TILE

def cell_from_world(x, y):      # Pixel coordinate to Grid coordinate
    return int(x // TILE), int(y // TILE)

def world_from_cell(c, r):      
    return (c*TILE + TILE*0.5, r*TILE + TILE*0.5)

def passable_cell(grid, c, r):
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
        return grid[r][c] not in ('#', 's')
    return False

def astar(grid, start_cell, goal_cell):     # Path finding function
    sx, sy = start_cell
    gx, gy = goal_cell

    # Early exit
    if (sx, sy) == (gx, gy): 
        return [world_from_cell(sx, sy)]
    if not passable_cell(grid, gx, gy): 
        return []
    
    # Evaluate distance between two grid
    def h(a,b): 
        return abs(a[0]-b[0]) + abs(a[1]-b[1])
    
    openh = []
    heapq.heappush(openh, (h((sx,sy),(gx,gy)) ,0 , (sx,sy)))    # openh is now a min-heap, the grid is stored and evaluated by the following form: (f, g, coordinate)
                                                                # f = g + h (the distance of the grid to goal), g is number of steps so far
    came = {}   # The node been passed                          
    g = {(sx,sy):0}    # The dictionary storing the best-known step cost to reach each grid

    while openh:
        _, gc, cur = heapq.heappop(openh)   # Poping from a min-heap gives the choice of smallest "h((sx,sy),(gx,gy))" (the distance)

        if cur == (gx, gy):     # If the path have reached the goal, return the path
            path = [cur]
            while cur in came:
                cur = came[cur]
                path.append(cur)    # Add the passed node into path
            path.reverse()  # Now from start to end
            return [world_from_cell(c,r) for (c,r) in path]     
        
        cx,cy = cur
        for nx,ny in ((cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)):     #  Explore the 4 neighbors of the current grid
            if not passable_cell(grid,nx,ny): 
                continue
            ng = gc + 1     # Next g (step + 1)
            if (nx,ny) not in g or ng < g[(nx,ny)]:     # If the neighbor not in g (not traversed yet), add it; If the neighbor is recorded in g but now the new path has a lower step cost, then update the new cost
                g[(nx,ny)] = ng
                came[(nx,ny)] = cur
                heapq.heappush(openh,(ng + h((nx,ny),(gx,gy)), ng ,(nx,ny)))    # Push the new grid into heap
                
    return []
