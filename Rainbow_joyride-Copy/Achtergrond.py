# Achtergrond.py
import pygame
from Startup import *
from player_colors import *

# Pas dit pad aan als jouw bestand anders heet of in een submap staat:
BACKGROUND_PATH = "projectweek-team_7\\Rainbow_joyride-Copy\\Background\\background\\content.png"

background, bg_loaded = load_image(BACKGROUND_PATH, (WIDTH, HEIGHT))

def draw_background():
    if bg_loaded and background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BLUE)
