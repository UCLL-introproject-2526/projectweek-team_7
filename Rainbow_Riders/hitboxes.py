# hitboxes.py
import pygame
import math
from audio import *
from Startup import *
from player import *


def player_rect(px, py):
    return pygame.Rect(px + 5, py + 5, PLAYER_W - 10, PLAYER_H - 10)

def obstacle_rect(obs):
    
    if obs["type"] == "float":
        return pygame.Rect(
            obs["x"] + 8,
            obs["y"] + 8,
            obs["s"] - 20,
            obs["s"] - 20
        )

    elif obs["type"] == "rainbow":
        # Rainbow heeft dezelfde afmetingen en positie als top/bottom
        if obs["position"] == "top":
            return pygame.Rect(obs["x"], 0, 70, obs["h"])
        else:  # bottom
            return pygame.Rect(obs["x"], HEIGHT - obs["h"], 70, obs["h"])
    else:  # laser - return None, we gebruiken custom collision
        return None
    
def coin_rect(coin):
    return pygame.Rect(coin["x"] - 12, coin["y"] - 12, 24, 24)

def check_laser_collision(px, py, obs):
    """Speciale collision check voor laser obstacles"""
    center_x = obs["x"] + 25
    center_y = obs["y"]

# Check of speler het centrum raakt
    dx = px + PLAYER_W/2 - center_x
    dy = py + PLAYER_H/2 - center_y
    if math.sqrt(dx*dx + dy*dy) < 15 + PLAYER_W/2:
        return True

# Check of speler de laser straal raakt
    rad = math.radians(obs["angle"])
    for i in range(0, int(obs["length"]), 5):
        lx = center_x + math.cos(rad) * i
        ly = center_y + math.sin(rad) * i

        if (px < lx < px + PLAYER_W and py < ly < py + PLAYER_H):
            return True

    return False

def check_collision(px, py, obstacles):
    p = player_rect(px, py)
    for obs in obstacles:
        if obs["type"] == "laser":
            if check_laser_collision(px, py, obs):
                return True
        else:
            # Normale collision voor andere obstakels
            if p.colliderect(obstacle_rect(obs)):
                game_over_sound()
                return True
    return False