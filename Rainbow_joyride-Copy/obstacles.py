# obstacles.py
import random
import pygame

from Startup import WIDTH, HEIGHT, screen
from player_colors import RED, YELLOW, PURPLE

def spawn_obstacle():
    obs_type = random.choice(["top", "bottom", "float"])
    if obs_type == "top":
        return {"type": "top", "x": WIDTH, "h": random.randint(100, 250)}
    elif obs_type == "bottom":
        return {"type": "bottom", "x": WIDTH, "h": random.randint(100, 250)}
    else:
        return {"type": "float", "x": WIDTH, "y": random.randint(100, HEIGHT - 150), "s": random.randint(60, 100)}

def draw_obstacle(obs):
    if obs["type"] == "top":
        pygame.draw.rect(screen, RED, (obs["x"], 0, 50, obs["h"]))
        pygame.draw.rect(screen, YELLOW, (obs["x"], obs["h"] - 10, 50, 10))
    elif obs["type"] == "bottom":
        y = HEIGHT - obs["h"]
        pygame.draw.rect(screen, RED, (obs["x"], y, 50, obs["h"]))
        pygame.draw.rect(screen, YELLOW, (obs["x"], y, 50, 10))
    else:
        pygame.draw.rect(screen, PURPLE, (obs["x"], obs["y"], obs["s"], obs["s"]))
        pygame.draw.rect(screen, YELLOW, (obs["x"] + 5, obs["y"] + 5, obs["s"] - 10, obs["s"] - 10), 2)

def move_obstacles(obstacles, speed):
    for obs in obstacles:
        obs["x"] -= speed
    return [o for o in obstacles if o["x"] > -100]
