import random
import pygame
import math

from Startup import WIDTH, HEIGHT, screen
from player_colors import RED, YELLOW, PURPLE

def spawn_obstacle():
    obs_type = random.choice(["top", "bottom", "float", "laser"])
    if obs_type == "top":
        return {"type": "top", "x": WIDTH, "h": random.randint(200, 350)}
    elif obs_type == "bottom":
        return {"type": "bottom", "x": WIDTH, "h": random.randint(200, 350)}
    elif obs_type == "float":
        return {"type": "float", "x": WIDTH, "y": random.randint(200, HEIGHT - 150), "s": random.randint(100, 150)}
    else:
        return {
            "type": "laser",
            "x": WIDTH,
            "y": random.randint(100, HEIGHT - 150),
            "angle": 0,
            "length": 170,
            "rotation_speed": random.choice([3, -3, 4, -4])
        }

def draw_obstacle(obs):
    if obs["type"] == "top":
        pygame.draw.rect(screen, RED, (obs["x"], 0, 50, obs["h"]))
        pygame.draw.rect(screen, YELLOW, (obs["x"], obs["h"] - 10, 50, 10))
    elif obs["type"] == "bottom":
        y = HEIGHT - obs["h"]
        pygame.draw.rect(screen, RED, (obs["x"], y, 50, obs["h"]))
        pygame.draw.rect(screen, YELLOW, (obs["x"], y, 50, 10))
    elif obs["type"] == "float":
        pygame.draw.rect(screen, PURPLE, (obs["x"], obs["y"], obs["s"], obs["s"]))
        pygame.draw.rect(screen, YELLOW, (obs["x"] + 5, obs["y"] + 5, obs["s"] - 10, obs["s"] - 10), 2)
    else:  # laser
        # Update rotatie
        obs["angle"] += obs["rotation_speed"]
        
        # Centrum van de laser
        center_x = obs["x"] + 25
        center_y = obs["y"]
        pygame.draw.circle(screen, (50, 110, 150), (int(center_x), int(center_y)), 15)
        
        # Bereken eindpunt van de laser
        rad = math.radians(obs["angle"])
        end_x = center_x + math.cos(rad) * obs["length"]
        end_y = center_y + math.sin(rad) * obs["length"]
        
        # Teken laser straal
        pygame.draw.line(screen, (50, 110, 150), (center_x, center_y), (end_x, end_y), 5)
        pygame.draw.line(screen, (50, 110, 150), (center_x, center_y), (end_x, end_y), 2)

def move_obstacles(obstacles, speed):
    for obs in obstacles:
        obs["x"] -= speed
    return [o for o in obstacles if o["x"] > -100]