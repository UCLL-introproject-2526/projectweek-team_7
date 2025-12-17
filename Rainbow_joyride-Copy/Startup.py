# Startup.py
import pygame

pygame.init()


pygame.mixer.init()
# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RAINBOW RIDERS")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 60)
font_small = pygame.font.Font(None, 24)

def load_image(path: str, size=None):
    """Laad een afbeelding, schaal optioneel. Geeft (surface, loaded_bool)."""
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img, True
    except Exception:
        return None, False
