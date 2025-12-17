# Achtergrond.py
import pygame
from Startup import WIDTH, HEIGHT, screen, load_image
from player_colors import BLUE

# Pas dit pad aan als jouw bestand anders heet of in een submap staat:
BACKGROUND_PATH = "C:\\Users\\Sonninberge\\github-classroom\\UCLL-introproject-2526\\projectweek-team_7\\Rainbow_joyride-Copy\Background\\background\content.png"

background, bg_loaded = load_image(BACKGROUND_PATH, (WIDTH, HEIGHT))

def draw_background():
    if bg_loaded and background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BLUE)
