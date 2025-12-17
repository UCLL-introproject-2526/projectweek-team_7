# hitboxes.py
import pygame
from Startup import HEIGHT
from player import PLAYER_W, PLAYER_H

def player_rect(px, py):
    # iets strakker voor collision
    return pygame.Rect(px + 5, py + 5, PLAYER_W - 10, PLAYER_H - 10)

def obstacle_rect(obs):
    if obs["type"] == "top":
        return pygame.Rect(obs["x"], 0, 50, obs["h"])
    elif obs["type"] == "bottom":
        return pygame.Rect(obs["x"], HEIGHT - obs["h"], 50, obs["h"])
    else:
        return pygame.Rect(obs["x"], obs["y"], obs["s"], obs["s"])

def coin_rect(coin):
    return pygame.Rect(coin["x"] - 12, coin["y"] - 12, 24, 24)
