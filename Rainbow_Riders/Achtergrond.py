from Startup import *
from player_colors import *

BACKGROUND_PATH = "Rainbow_Riders\\Assets\\background\\background_image.png"
BG_SPEED = 2
background, bg_loaded = load_image(BACKGROUND_PATH, (WIDTH, HEIGHT))

# x-positie van de achtergrond
bg_x = 0

def draw_background():
    global bg_x

    if bg_loaded and background:
        # beweeg achtergrond naar links
        bg_x -= BG_SPEED

        # reset zodra hij volledig uit beeld is
        if bg_x <= -WIDTH:
            bg_x = 0

        # teken twee achtergronden naast elkaar
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + WIDTH, 0))
    else:
        screen.fill(BLUE)