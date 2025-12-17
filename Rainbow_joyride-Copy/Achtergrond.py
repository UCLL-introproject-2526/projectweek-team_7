# Achtergrond.py
import pygame
from Startup import *
from player_colors import *

BACKGROUND_PATH = "Rainbow_joyride-Copy\\Background\\background\\content.png"

background, bg_loaded = load_image(BACKGROUND_PATH, (WIDTH, HEIGHT))

# x-positie van de achtergrond
bg_x = 0

def draw_background():
    global bg_x
    if bg_loaded and background:
        screen.blit(background, (bg_x, 0))
        screen.blit(background, (bg_x + WIDTH, 0))  # tweede achtergrond
    else:
        screen.fill(BLUE)
