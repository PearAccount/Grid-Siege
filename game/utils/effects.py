from ..settings import SHAKE_DECAY, CROSSHAIR_PULSE_DECAY

shake_mag = 0.0
crosshair_pulse = 0.0
def add_shake(mag: float):
    global shake_mag
    shake_mag += mag

def update_shake(dt: float):
    global shake_mag
    if shake_mag <= 0: 
        return (0.0, 0.0)
    shake_mag = max(0.0, shake_mag - SHAKE_DECAY * dt)
    import random as _r
    return (_r.uniform(-1.0,1.0) * shake_mag, _r.uniform(-1.0,1.0) * shake_mag)

def add_crosshair_pulse(amount: float):
    global crosshair_pulse
    crosshair_pulse += amount

def update_crosshair_pulse(dt: float) -> float:
    global crosshair_pulse
    p = crosshair_pulse
    crosshair_pulse = max(0.0, crosshair_pulse - CROSSHAIR_PULSE_DECAY * dt)
    return p
