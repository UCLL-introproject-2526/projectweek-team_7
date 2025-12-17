# Achtergrond.py
import pygame
from Startup import screen, WIDTH, HEIGHT

try:
    background = pygame.image.load("content.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    bg_loaded = True
except:
    background = None
    bg_loaded = False

def draw_background():
    if bg_loaded:
        screen.blit(background, (0, 0))
    else:
        screen.fill((52, 152, 219))  # blauw
