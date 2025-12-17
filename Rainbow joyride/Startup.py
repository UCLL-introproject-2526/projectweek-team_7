import pygame

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
GRAY = (80, 80, 80)

# Screen & clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rainbow Riders")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 60)
font_small = pygame.font.Font(None, 24)
