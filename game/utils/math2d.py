import math
def v_add(a,b): 
    return (a[0]+b[0], a[1]+b[1])
def v_sub(a,b): 
    return (a[0]-b[0], a[1]-b[1])
def v_len(a): 
    return math.hypot(a[0], a[1])
def v_norm(a):
    l = v_len(a)
    return (a[0]/l, a[1]/l) if l else (0.0, 0.0)
