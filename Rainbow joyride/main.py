import pygame
import random
import sys

from Achtergrond import 
import coins
import hitboxes
import menu
import obstacles
import player_colors
import player
import Startup
import states
# Initialize
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
GRAY = (80, 80, 80)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jetpack Joyride")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Load player image
try:
    # Probeer de afbeelding te laden (pas het pad aan naar jouw bestand!)
    player_image = pygame.image.load("C:\\school\\projectweek\\small_game\\avatar_zonder_vlam.png")  # Verander dit naar jouw bestandsnaam
    # Schaal de afbeelding naar de gewenste grootte
    player_image = pygame.transform.scale(player_image, (60, 80))
    image_loaded = True
except:
    print("Kon afbeelding niet laden. Gebruik fallback tekening.")
    player_image = None
    image_loaded = False

# Player
player_x = 100
player_y = HEIGHT - 150
player_w, player_h = 60, 80  # Aangepast aan de nieuwe grootte
player_vel = 0
GRAVITY = 0.8
THRUST = -12

# Game state
game_active = False
score = 0
coins = 0
speed = 4
obstacles = []
coin_items = []
spawn_timer = 0

def draw_player_fallback(x, y, thrusting):
    """Fallback tekening als de afbeelding niet laadt"""
    # Body
    pygame.draw.rect(screen, (139, 69, 19), (x, y, 40, 60), border_radius=5)
    # Head
    pygame.draw.circle(screen, (255, 200, 150), (x + 20, y - 10), 15)
    # Goggles
    pygame.draw.circle(screen, BLACK, (x + 20, y - 10), 8)
    # Jetpack flames
    if thrusting:
        flame_y = y + 60
        for i in range(3):
            offset = random.randint(-5, 5)
            pygame.draw.circle(screen, YELLOW, (x + 20 + offset, flame_y + i*5), 8 - i*2)

def draw_player(x, y, thrusting):
    """Teken de speler met afbeelding of fallback"""
    if image_loaded and player_image:
        # Teken de afbeelding
        screen.blit(player_image, (x, y))
        
        # Voeg nog steeds de jetpack vlammen toe als je drukt
        if thrusting:
            flame_y = y + player_h
            for i in range(3):
                offset = random.randint(-5, 5)
                pygame.draw.circle(screen, YELLOW, (x + player_w//2 + offset, flame_y + i*5), 8 - i*2)
                pygame.draw.circle(screen, RED, (x + player_w//2 + offset, flame_y + i*5), 4 - i)
    else:
        draw_player_fallback(x, y, thrusting)

def draw_obstacle(obs):
    if obs['type'] == 'top':
        pygame.draw.rect(screen, RED, (obs['x'], 0, 50, obs['h']))
        pygame.draw.rect(screen, YELLOW, (obs['x'], obs['h']-10, 50, 10))
    elif obs['type'] == 'bottom':
        y = HEIGHT - obs['h']
        pygame.draw.rect(screen, RED, (obs['x'], y, 50, obs['h']))
        pygame.draw.rect(screen, YELLOW, (obs['x'], y, 50, 10))
    else:  # floating
        pygame.draw.rect(screen, (128, 0, 128), (obs['x'], obs['y'], obs['s'], obs['s']))
        pygame.draw.rect(screen, YELLOW, (obs['x']+5, obs['y']+5, obs['s']-10, obs['s']-10), 2)

def draw_coin(coin):
    pygame.draw.circle(screen, YELLOW, (coin['x'], coin['y']), 12)
    pygame.draw.circle(screen, (200, 150, 0), (coin['x'], coin['y']), 10)
    text = font_small.render("$", True, BLACK)
    screen.blit(text, (coin['x']-6, coin['y']-10))

def spawn_obstacle():
    obs_type = random.choice(['top', 'bottom', 'float'])
    if obs_type == 'top':
        return {'type': 'top', 'x': WIDTH, 'h': random.randint(100, 250)}
    elif obs_type == 'bottom':
        return {'type': 'bottom', 'x': WIDTH, 'h': random.randint(100, 250)}
    else:
        return {'type': 'float', 'x': WIDTH, 'y': random.randint(100, HEIGHT-150), 's': random.randint(60, 100)}

def spawn_coin():
    return {'x': WIDTH, 'y': random.randint(50, HEIGHT-100)}

def check_collision(px, py):
    player_rect = pygame.Rect(px+5, py+5, player_w-10, player_h-10)
    for obs in obstacles:
        if obs['type'] == 'top':
            obs_rect = pygame.Rect(obs['x'], 0, 50, obs['h'])
        elif obs['type'] == 'bottom':
            obs_rect = pygame.Rect(obs['x'], HEIGHT - obs['h'], 50, obs['h'])
        else:
            obs_rect = pygame.Rect(obs['x'], obs['y'], obs['s'], obs['s'])
        
        if player_rect.colliderect(obs_rect):
            return True
    return False

def check_coin_collect(px, py):
    global coins, score
    player_rect = pygame.Rect(px, py, player_w, player_h)
    to_remove = []
    for coin in coin_items:
        coin_rect = pygame.Rect(coin['x']-12, coin['y']-12, 24, 24)
        if player_rect.colliderect(coin_rect):
            coins += 1
            score += 10
            to_remove.append(coin)
    
    for coin in to_remove:
        coin_items.remove(coin)

def draw_menu():
    Achtergrond.draw_background()

    
    # Title
    title = font.render("RAINBOW RIDERS", True, YELLOW)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    # Player preview
    draw_player(WIDTH//2 - player_w//2, 200, False)
    
    # Instructions
    inst = font_small.render("Klik of druk SPATIE om te vliegen", True, WHITE)
    screen.blit(inst, (WIDTH//2 - inst.get_width()//2, 320))
    
    # Start button
    button_rect = pygame.Rect(WIDTH//2 - 100, 400, 200, 60)
    pygame.draw.rect(screen, GREEN, button_rect, border_radius=10)
    start_text = font.render("START", True, WHITE)
    screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, 415))
    
    # Coins display
    coin_text = font_small.render(f"Munten: {coins}", True, YELLOW)
    screen.blit(coin_text, (20, 20))
    
    return button_rect

def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Game Over text
    go_text = font.render("GAME OVER!", True, RED)
    screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, 150))
    
    # Score
    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 220))
    coin_text = font.render(f"Munten: {coins}", True, YELLOW)
    screen.blit(coin_text, (WIDTH//2 - coin_text.get_width()//2, 270))
    
    # Retry button
    retry_rect = pygame.Rect(WIDTH//2 - 150, 350, 120, 50)
    menu_rect = pygame.Rect(WIDTH//2 + 30, 350, 120, 50)
    
    pygame.draw.rect(screen, GREEN, retry_rect, border_radius=5)
    pygame.draw.rect(screen, BLUE, menu_rect, border_radius=5)
    
    retry_text = font_small.render("OPNIEUW", True, WHITE)
    menu_text = font_small.render("MENU", True, WHITE)
    
    screen.blit(retry_text, (retry_rect.centerx - retry_text.get_width()//2, retry_rect.centery - 10))
    screen.blit(menu_text, (menu_rect.centerx - menu_text.get_width()//2, menu_rect.centery - 10))
    
    return retry_rect, menu_rect

def reset_game():
    global player_y, player_vel, score, speed, obstacles, coin_items, spawn_timer
    player_y = HEIGHT - 150
    player_vel = 0
    score = 0
    speed = 5
    obstacles = []
    coin_items = []
    spawn_timer = 0

# Main game loop
running = True
thrusting = False
game_over = False
start_button = None

while running:
    dt = clock.tick(FPS) / 60.0
    
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if not game_active:
                if start_button and start_button.collidepoint(mouse_pos):
                    game_active = True
                    game_over = False
                    reset_game()
            elif game_active and not game_over:
                thrusting = True
            elif game_over:
                retry, menu = draw_game_over()
                if retry.collidepoint(mouse_pos):
                    game_over = False
                    reset_game()
                elif menu.collidepoint(mouse_pos):
                    game_active = False
                    game_over = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            thrusting = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active and not game_over:
                thrusting = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                thrusting = False
    
    # Game logic
    if game_active and not game_over:
        # Player physics
        if thrusting:
            player_vel = THRUST
        else:
            player_vel += GRAVITY
        
        player_vel = max(-15, min(15, player_vel))
        player_y += player_vel
        
        # Boundaries
        if player_y < 20:
            player_y = 20
            player_vel = 0
        if player_y > HEIGHT - player_h - 20:
            player_y = HEIGHT - player_h - 20
            player_vel = 0
        
        # Spawn obstacles and coins
        spawn_timer += 1
        if spawn_timer > 60:
            obstacles.append(spawn_obstacle())
            spawn_timer = 0
        
        if random.random() < 0.02:
            coin_items.append(spawn_coin())
        
        # Move obstacles
        for obs in obstacles:
            obs['x'] -= speed
        obstacles = [o for o in obstacles if o['x'] > -100]
        
        # Move coins
        for coin in coin_items:
            coin['x'] -= speed
        coin_items = [c for c in coin_items if c['x'] > -50]
        
        # Check collisions
        if check_collision(player_x, player_y):
            game_over = True
        
        check_coin_collect(player_x, player_y)
        
        # Update score
        score += 0.1
        speed = min(5 + score/200, 10)
    
    # Drawing
    if game_active:
        Achtergrond.draw_background()


        
        # Ground and ceiling
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 20))
        pygame.draw.rect(screen, GRAY, (0, HEIGHT-20, WIDTH, 20))
        
        # Draw game objects
        for obs in obstacles:
            draw_obstacle(obs)
        
        for coin in coin_items:
            draw_coin(coin)
        
        draw_player(player_x, player_y, thrusting)
        
        # HUD
        score_text = font_small.render(f"Score: {int(score)}", True, WHITE)
        coin_text = font_small.render(f"Munten: {coins}", True, YELLOW)
        screen.blit(score_text, (10, 10))
        screen.blit(coin_text, (10, 35))
        
        if game_over:
            draw_game_over()
    else:
        start_button = draw_menu()
    
    pygame.display.flip()

pygame.quit()
sys.exit()