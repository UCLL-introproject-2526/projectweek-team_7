# menu.py
import pygame

from Startup import *
from player_colors import *
from Achtergrond import *
from audio import *

menu_background = pygame.image.load(
    "Rainbow_joyride-Copy\\Background\\background\\menuschermpje.png"
).convert()

menu_background = pygame.transform.scale(
    menu_background, (WIDTH, HEIGHT)
)

def draw_menu(coins_total, player_w, player_h):
    screen.blit(menu_background, (0, 0))


    title = font.render(" ", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))


    inst = font_small.render(" ", True, WHITE)
    screen.blit(inst, (WIDTH // 2 - inst.get_width() // 2, 320))

    button_rect = pygame.Rect(WIDTH // 2 - 100, 473, 200, 60)
    pygame.draw.rect(screen, GREEN, button_rect, border_radius=10)
    start_text = font.render("START", True, WHITE)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 485))

    coin_text = font_small.render(f"Munten: {coins_total}", True, YELLOW)
    screen.blit(coin_text, (20, 20))

    return button_rect

def draw_game_over(score, coins_total):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    go_text = font.render("GAME OVER!", True, RED)
    screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, 150))

    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 220))

    coin_text = font.render(f"Munten: {coins_total}", True, YELLOW)
    screen.blit(coin_text, (WIDTH // 2 - coin_text.get_width() // 2, 270))

    retry_rect = pygame.Rect(WIDTH // 2 - 150, 350, 120, 50)
    menu_rect = pygame.Rect(WIDTH // 2 + 30, 350, 120, 50)

    pygame.draw.rect(screen, GREEN, retry_rect, border_radius=5)
    pygame.draw.rect(screen, BLUE, menu_rect, border_radius=5)

    retry_text = font_small.render("OPNIEUW", True, WHITE)
    menu_text = font_small.render("MENU", True, WHITE)

    screen.blit(retry_text, (retry_rect.centerx - retry_text.get_width() // 2, retry_rect.centery - 10))
    screen.blit(menu_text, (menu_rect.centerx - menu_text.get_width() // 2, menu_rect.centery - 10))

    return retry_rect, menu_rect
