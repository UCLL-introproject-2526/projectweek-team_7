# looper.py
from Achtergrond import bg_x
from Startup import WIDTH

SCROLL_SPEED = 5

def update_background():
    global bg_x
    bg_x -= SCROLL_SPEED

    # als de achtergrond helemaal weg is
    if bg_x <= -WIDTH:
        bg_x = 0    
