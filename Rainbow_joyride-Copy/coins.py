# coins.py
import random
import pygame

from Startup import WIDTH, HEIGHT, screen, font_small
from player_colors import YELLOW, BLACK

def spawn_coin():
    return {"x": WIDTH, "y": random.randint(50, HEIGHT - 100)}

def draw_coin(coin):
    pygame.draw.circle(screen, YELLOW, (coin["x"], coin["y"]), 12)
    pygame.draw.circle(screen, (200, 150, 0), (coin["x"], coin["y"]), 10)
    text = font_small.render("$", True, BLACK)
    screen.blit(text, (coin["x"] - 6, coin["y"] - 10))

def move_coins(coin_items, speed):
    for c in coin_items:
        c["x"] -= speed
    return [c for c in coin_items if c["x"] > -50]
