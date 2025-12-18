# Startup.py
import pygame

pygame.init()
pygame.mixer.init()

loading_background = None
MIN_LOADING_TIME = 3000
visual_progress = 0

# Constants
WIDTH, HEIGHT = 1138, 650
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


def startup_loading_screen(load_functions):
    total = len(load_functions)
    loaded = 0
    start_time = pygame.time.get_ticks()
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if loaded < total:
            load_functions[loaded]()
            loaded += 1

        progress = loaded / total if total > 0 else 1
        elapsed = pygame.time.get_ticks() - start_time

        # forceer minimum tijd
        if progress >= 1 and elapsed >= MIN_LOADING_TIME:
            running = False

        if loading_background:
            screen.blit(loading_background, (0, 0))
        else:
            screen.fill((10, 10, 30))

        title = font.render("RAINBOW RIDERS", True, (255, 255, 255))
        screen.blit(
            title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 120)
        )

        draw_loading_bar(min(progress, elapsed / MIN_LOADING_TIME))
        pygame.display.flip()


def draw_loading_bar(progress):
    bar_width = 600
    bar_height = 30
    x = (WIDTH - bar_width) // 2
    y = HEIGHT // 2

    pygame.draw.rect(screen, (60, 60, 60), (x, y, bar_width, bar_height))
    pygame.draw.rect(
        screen, (0, 200, 255), (x, y, int(bar_width * progress), bar_height)
    )

    percent = font_small.render(f"{int(progress * 100)}%", True, (255, 255, 255))
    screen.blit(percent, (x + bar_width // 2 - 10, y - 30))


def load_images():
    global loading_background
    # Laad de afbeelding en schaal deze naar de schermgrootte
    loading_background = pygame.image.load(
        "Rainbow_joyride-Copy\\Background\\background\\loadingscreen.png"
    ).convert_alpha()
    loading_background = pygame.transform.scale(loading_background, (WIDTH, HEIGHT))


def load_audio():
    pygame.mixer.music.load("Rainbow_joyride-Copy\\audio\\replaceholder1.mp3")


def load_fonts():
    pygame.font.Font(None, 24)