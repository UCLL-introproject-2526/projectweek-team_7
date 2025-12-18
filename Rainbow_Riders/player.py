import random
import pygame

from Startup import *
from player_colors import *

PLAYER_IMG_PATH = "Rainbow_Riders\\Background\Player-images\\avatar_zonder_vlam.png"
PLAYER_SIZE = (60, 80)

player_image, image_loaded = load_image(PLAYER_IMG_PATH, PLAYER_SIZE)

# Player constants
GRAVITY = 0.6
THRUST = -12

PLAYER_W, PLAYER_H = PLAYER_SIZE

def draw_player_fallback(x, y, thrusting):
    # lichaam
    pygame.draw.rect(screen, (139, 69, 19), (x, y, 40, 60), border_radius=5)
    # hoofd
    pygame.draw.circle(screen, (255, 200, 150), (x + 20, y - 10), 15)
    # bril
    pygame.draw.circle(screen, BLACK, (x + 20, y - 10), 8)
    # vlammen
    if thrusting:
        flame_y = y + 60
        for i in range(3):
            offset = random.randint(-5, 5)
            pygame.draw.circle(screen, YELLOW, (x + 20 + offset, flame_y + i * 5), 8 - i * 2)

def draw_player(x, y, thrusting):
    if image_loaded and player_image:
        screen.blit(player_image, (x, y))

        if thrusting:
            flame_y = y + PLAYER_H
            for i in range(3):
                offset = random.randint(-5, 5)
                pygame.draw.circle(screen, YELLOW, (x + PLAYER_W // 2 + offset, flame_y + i * 5), 8 - i * 2)
                pygame.draw.circle(screen, RED, (x + PLAYER_W // 2 + offset, flame_y + i * 5), 4 - i)
    else:
        draw_player_fallback(x, y, thrusting)

def apply_physics(player_y, player_vel, thrusting):
    """Geeft (new_y, new_vel) terug."""
    if thrusting:
        player_vel = THRUST
    else:
        player_vel += GRAVITY

    player_vel = max(-15, min(15, player_vel))
    player_y += player_vel

    # grenzen
    if player_y < 10:
        player_y = 10
        player_vel = 0
    if player_y > HEIGHT - PLAYER_H - 10:
        player_y = HEIGHT - PLAYER_H - 10
        player_vel = 0

    return player_y, player_vel
