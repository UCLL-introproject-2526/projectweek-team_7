import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# --- Initialiseer de Mixer (Belangrijk!) ---
pygame.mixer.init()

MUSIC_FILE = 'programming 1/audio/Cyberpunk Moonlight Sonata.mp3' # Pas het pad en de naam aan!

def start_background_music():
    """Laadt de muziek en begint met afspelen in een lus (-1)."""
    global MUSIC_FILE
    
    try:
        # Laad de muziek
        pygame.mixer.music.load(MUSIC_FILE)
        
        # Start de muziek: -1 betekent oneindig herhalen
        pygame.mixer.music.play(-1) 
        
        # Optioneel: Stel het volume in (0.0 tot 1.0)
        pygame.mixer.music.set_volume(0.5) 
        print(f"Achtergrondmuziek '{MUSIC_FILE}' gestart.")
        
    except pygame.error as e:
        print(f"Fout bij het laden of afspelen van muziek: {e}")
        print("Controleer of het bestandspad en het formaat correct zijn.")

# --- In de hoofdsectie van uw script (na de functie definities) ---

# ...

# --- ROEP DE MUZIEK START FUNCTIE HIER AAN ---
start_background_music()
# --------------------------------------------

# Start de hoofdloop
# --- Game Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jetpack Joyride Pygame")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
GREEN = (46, 204, 113)
GRAY_FLOOR = (80, 80, 80)
GRAY_CEILING = (80, 80, 80)
DARK_BLUE = (30, 40, 80) # For background
MENU_PANEL = (40, 50, 90) # For panel background
BUTTON_GREEN = (76, 175, 80)

# --- Nieuwe sectie: Achtergrondafbeelding laden ---
try:
    # Probeer de achtergrondafbeelding te laden uit de map 'background'
    # Pas 'achtergrond.jpg' aan naar de daadwerkelijke naam van uw bestand
    BACKGROUND_IMAGE = pygame.image.load('programming 1/background/achtergrond.jpg').convert() 
    # Schaal de afbeelding naar de schermgrootte
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background_loaded = True
    print("Achtergrondafbeelding geladen.")
except pygame.error as e:
    print(f"Fout bij het laden van de achtergrondafbeelding: {e}. Standaard kleur wordt gebruikt.")
    BACKGROUND_IMAGE = None
    background_loaded = False
# --- Einde van nieuwe sectie ---

# Game Physics / State Initialization
FPS = 60
clock = pygame.time.Clock()

# Player Constants
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 100
PLAYER_START_X = 120
GROUND_Y = SCREEN_HEIGHT - 16 - PLAYER_HEIGHT
CEILING_Y = 16


# --- NIEUW: Spelerafbeelding Laden ---
try:
    # Zorg ervoor dat u een map genaamd 'sprites' heeft
    # en dat de afbeelding daar is opgeslagen (bijv. 'barry_jetpack.png')
    PLAYER_IMAGE = pygame.image.load('programming 1/sprites/barry_jetpack.png').convert_alpha() 
    # Schaal de afbeelding naar de juiste grootte
    PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT + 10))
    
    # Optioneel: Maak een 'thrusting' versie (met vlammen)
    # Dit is een simpele manier: we kantelen de afbeelding iets als de speler stuwt
    PLAYER_THRUST_IMAGE = pygame.transform.rotate(PLAYER_IMAGE, 10) 
    
    player_image_loaded = True
    print("Spelerafbeelding geladen.")
except pygame.error as e:
    print(f"Fout bij het laden van de spelerafbeelding: {e}. Standaard gekleurde speler wordt gebruikt.")
    PLAYER_IMAGE = None
    player_image_loaded = False
# --- Einde Spelerafbeelding Laden ---

# Game Variables
game_state = 'menu' # Can be 'menu', 'playing', 'gadgets'
coins = 0
score = 0
high_score = 0
player_y = GROUND_Y
velocity = 0
BASE_SPEED = 25.0 
speed = BASE_SPEED 
is_thrusting = False
is_speed_boosting = False
obstacles = []
coin_items = []
game_over = False
distance = 0
zapper_count = 0 
current_tick = 0 # Added for time-dependent obstacle movement

# Physics constants
# --- ADJUSTED: Increased GRAVITY and THRUST_POWER for faster vertical response ---
GRAVITY = 2  # Increased from 0.8
THRUST_POWER = -16 # Increased from -8
MAX_VELOCITY = 36 # Slight increase to accommodate higher forces

# Timing for Spawning (in frames)
# --- ADJUSTED: Reduced spawn rate for more obstacles ---
<<<<<<< HEAD:test/programming 1/jetpack.py
OBSTACLE_SPAWN_RATE = int(0.4 * FPS) # Reduced from 1.4 * FPS
COIN_SPAWN_RATE = int(1.2 * FPS)
=======
OBSTACLE_SPAWN_RATE = int(0.3 * FPS) # Reduced from 1.4 * FPS
COIN_SPAWN_RATE = int(0.4 * FPS)
>>>>>>> 6079e424125df335879ca8ab12595b095600fb00:programming 1/jetpack.py
obstacle_spawn_counter = OBSTACLE_SPAWN_RATE
coin_spawn_counter = COIN_SPAWN_RATE

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# --- Missions & Gadgets Data Structures ---
MISSIONS = [
    {'id': 1, 'desc': "COLLECT 500 COINS", 'target': 500, 'progress': 0, 'reward': 500, 'completed': False},
    {'id': 2, 'desc': "FLY 1000M IN ONE RUN", 'target': 1000, 'progress': 0, 'reward': 1000, 'completed': False},
    {'id': 3, 'desc': "DEFEAT 5 ZAPPERS (WIP)", 'target': 5, 'progress': 0, 'reward': 750, 'completed': False}
]

GADGETS = [
    {'name': 'Coin Magnet', 'price': 5000, 'purchased': False, 'active': False, 'magnet_range': 200}, 
    {'name': 'Force Shield', 'price': 8000, 'purchased': False, 'active': False},
    {'name': 'Speed Boost', 'price': 8000, 'purchased': False, 'active': False, 'speed_multiplier': 1.8}
]

# --- Character Looks Data Structure ---
CHARACTER_LOOKS = [
    {'id': 0, 'name': 'Classic Barry', 'price': 0, 'purchased': True, 'active': True, 'color': (139, 69, 19)},
    {'id': 1, 'name': 'Red Suit', 'price': 2500, 'purchased': False, 'active': False, 'color': (200, 50, 50)},
    {'id': 2, 'name': 'Green Suit', 'price': 2500, 'purchased': False, 'active': False, 'color': (50, 200, 50)},
]

# Function to get the current active look
def get_active_look():
    for look in CHARACTER_LOOKS:
        if look['active']:
            return look
    return CHARACTER_LOOKS[0] # Fallback

# --- Utility Functions ---

# --- Utility Functions (draw_player AANGEPAST) ---

def draw_player(surface, x, y, thrusting):
    """Draws the player using an image if loaded, otherwise uses the colored box."""
    
    global PLAYER_IMAGE, PLAYER_THRUST_IMAGE, player_image_loaded
    
    # Berekent de rect voor botsing en positie, ongeacht of de afbeelding wordt gebruikt
    player_rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    if player_image_loaded:
        # Teken de afbeelding
        # We gebruiken y-5 zodat de jetpack (die we extra hoogte hebben gegeven) niet door de grond gaat
        
        if thrusting:
            # Gebruik de kantelende afbeelding wanneer de speler stuwt
            img_to_use = PLAYER_THRUST_IMAGE
            # De blit-positie moet mogelijk worden aangepast vanwege de rotatie/afmetingen
            surface.blit(img_to_use, (x - 5, y - 5)) 
            
            # Teken een eenvoudig vlam-effect
            flame_height = random.randint(10, 20)
            flame_width = random.randint(8, 15)
            # Plaats de vlam onder de jetpack (links van de speler)
            flame_points = [
                (x - 10, y + 40), 
                (x - 10 - flame_width // 2, y + 40 + flame_height // 2),
                (x - 10, y + 40 + flame_height),
                (x - 10 + flame_width // 2, y + 40 + flame_height // 2)
            ]
            pygame.draw.polygon(surface, RED, flame_points)
            pygame.draw.polygon(surface, YELLOW, [(p[0], p[1]-2) for p in flame_points])
            
        else:
            # Standaard afbeelding
            img_to_use = PLAYER_IMAGE
            surface.blit(img_to_use, (x, y - 5)) 

    else:
        # Val terug op de gekleurde Pygame-box als de afbeelding niet is geladen
        active_look = get_active_look()
        suit_color = active_look['color']
        
        # Oude Pygame box tekenlogica (zoals eerder)
        pygame.draw.rect(surface, suit_color, player_rect, border_radius=5)
        pygame.draw.rect(surface, (60, 40, 20), (x+5, y, 30, 10)) # Baard
        pygame.draw.circle(surface, BLACK, (x + PLAYER_WIDTH // 2, y + 8), 10) # Goggles
        pygame.draw.circle(surface, (100, 200, 255), (x + PLAYER_WIDTH // 2, y + 8), 8)
        
        # Oude Jetpack en Vlammen logica
        pygame.draw.rect(surface, RED, (x - 10, y + 10, 10, 30), border_radius=3)
        pygame.draw.polygon(surface, WHITE, [(x - 10, y + 10), (x - 10, y + 40), (x - 20, y + 25)]) 
        
        if thrusting:
            flame_height = random.randint(15, 25)
            flame_width = random.randint(10, 20)
            flame_points = [
                (x - 5, y + 40), (x - 5 - flame_width // 2, y + 40 + flame_height // 2),
                (x - 5, y + 40 + flame_height), (x - 5 + flame_width // 2, y + 40 + flame_height // 2)
            ]
            pygame.draw.polygon(surface, RED, flame_points)
            pygame.draw.polygon(surface, YELLOW, [(p[0], p[1]-3) for p in flame_points])
            
    # Draw Coin Magnet Aura (deze blijft hetzelfde)
    magnet_gadget = next((g for g in GADGETS if g['name'] == 'Coin Magnet'), None)
    if magnet_gadget and magnet_gadget['purchased']:
        magnet_range = magnet_gadget['magnet_range']
        magnet_surface = pygame.Surface((magnet_range * 2, magnet_range * 2), pygame.SRCALPHA)
        pygame.draw.circle(magnet_surface, (0, 0, 0, 0), (magnet_range, magnet_range), magnet_range)
        SCREEN.blit(magnet_surface, (x + PLAYER_WIDTH // 2 - magnet_range, y + PLAYER_HEIGHT // 2 - magnet_range))

def draw_obstacle(surface, obstacle):
    x = int(obstacle['x'])
    obs_type = obstacle['type']
    
    if obs_type == 'top':
        height = int(obstacle['height'])
        rect = pygame.Rect(x, 16, 60, height)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, YELLOW, (x, 16 + height - 8, 60, 8))
        
    elif obs_type == 'bottom':
        height = int(obstacle['height'])
        y = SCREEN_HEIGHT - 16 - height
        rect = pygame.Rect(x, y, 60, height)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, YELLOW, (x, y, 60, 8))

    elif obs_type == 'floating':
        y = int(obstacle['y'])
        size = int(obstacle['size'])
        rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(surface, (128, 0, 128), rect) # Standard Zapper
        pygame.draw.rect(surface, YELLOW, (x+4, y+4, size-8, size-8), 2)
        
    # --- New: Rotating Laser ---
    elif obs_type == 'rotating_laser':
        center_x = x + obstacle['radius']
        center_y = obstacle['y']
        angle = obstacle['angle']
        
        # Draw base
        pygame.draw.circle(surface, (100, 100, 100), (center_x, center_y), 15)
        
        # Calculate laser endpoint
        end_x = center_x + obstacle['length'] * math.cos(math.radians(angle))
        end_y = center_y + obstacle['length'] * math.sin(math.radians(angle))
        
        # Draw laser beam (line)
        pygame.draw.line(surface, RED, (center_x, center_y), (end_x, end_y), 5)
        # Collision object is the line itself.

    # --- New: Moving Block (Up/Down) ---
    elif obs_type == 'moving_block':
        y = int(obstacle['current_y'])
        height = 60
        width = 60
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, (0, 0, 150), rect) # Dark Blue Block
        pygame.draw.rect(surface, (0, 0, 255), rect, 3)
        

def get_rotated_rect(center, length, angle):
    """Calculates the four corners of a line/rectangle rotated around a center point."""
    
    # We will approximate the laser collision as a wide line (4 points)
    p1 = (center[0], center[1])
    
    # Calculate end point
    end_x = center[0] + length * math.cos(math.radians(angle))
    end_y = center[1] + length * math.sin(math.radians(angle))
    p2 = (end_x, end_y)
    
    return p1, p2

def check_line_collision(p_rect, p1, p2):
    """Checks if a player rectangle collides with a line segment (simplified)."""
    # Simplified collision check for a line segment:
    # Check if the player rect intersects the bounding box of the line
    # AND check the distance from the center of the line to the player center (more complex)
    
    line_rect = pygame.Rect(min(p1[0], p2[0]), min(p1[1], p2[1]), 
                           abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
    
    # Add a buffer for the thickness of the line
    line_rect.inflate_ip(10, 10)
    
    if p_rect.colliderect(line_rect):
        # A more precise check is required for line collision, but for now, 
        # a bounding box check with buffer is a good start.
        # This will trigger collision if the player is near the laser line.
        return True
    return False

def draw_coin(surface, coin):
    x = int(coin['x'])
    y = int(coin['y'])
    highlight_color = YELLOW if not coin.get('pulling') else (255, 255, 150)
    
    pygame.draw.circle(surface, highlight_color, (x + 10, y + 10), 10)
    pygame.draw.circle(surface, (200, 150, 0), (x + 10, y + 10), 8)
    text = font_small.render("$", True, BLACK)
    surface.blit(text, (x + 5, y + 2))


def draw_hud(surface, score_val, coins_val, dist):
    pygame.draw.rect(surface, BLACK, (10, 10, 200, 80), border_radius=5)
    
    score_text = font_small.render(f"SCORE: {score_val}", True, YELLOW)
    surface.blit(score_text, (20, 20))
    
    dist_text = font_small.render(f"DISTANCE: {math.floor(dist)}m", True, YELLOW)
    surface.blit(dist_text, (20, 40))
    
    coin_text = font_small.render(f"COINS: {coins_val}", True, YELLOW)
    surface.blit(coin_text, (20, 60))

    global is_speed_boosting
    if is_speed_boosting:
        boost_text = font_small.render("SPEED BOOST ACTIVE", True, RED)
        surface.blit(boost_text, (SCREEN_WIDTH - boost_text.get_width() - 10, 20))


# --- Game Logic Functions ---

def update_player(dt):
    global velocity, player_y, game_over

    if is_thrusting:
        velocity = THRUST_POWER
    else:
        velocity += GRAVITY
    
    velocity = max(-MAX_VELOCITY, min(MAX_VELOCITY, velocity))
    player_y += velocity * dt
    
    if player_y > GROUND_Y:
        player_y = GROUND_Y
        velocity = 0
    elif player_y < CEILING_Y:
        player_y = CEILING_Y
        velocity = 0


def apply_coin_magnet(dt, player_center_x, player_center_y):
    """Pulls coins towards the player when the magnet is purchased."""
    global coin_items, coins, score
    
    magnet_gadget = next((g for g in GADGETS if g['name'] == 'Coin Magnet'), None)
    if not magnet_gadget or not magnet_gadget['purchased']:
        return

    magnet_range = magnet_gadget['magnet_range']
    magnet_force = 10.0 
    
    updated_coins = []
    
    for coin in coin_items:
        coin_center_x = coin['x'] + 10
        coin_center_y = coin['y'] + 10
        
        dx = player_center_x - coin_center_x
        dy = player_center_y - coin_center_y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist < magnet_range:
            coin['pulling'] = True
            
            if dist > 1: 
                coin['x'] += dx / dist * (speed * magnet_force) * dt 
                coin['y'] += dy / dist * (speed * magnet_force) * dt
            
            if dist < 30: 
                coins += 1
                score += 10
                MISSIONS[0]['progress'] = min(MISSIONS[0]['target'], MISSIONS[0]['progress'] + 1)
            else:
                updated_coins.append(coin) 
        elif coin['x'] > -50:
            coin['pulling'] = False
            updated_coins.append(coin) 
            
    coin_items = updated_coins


def update_elements(dt):
    global obstacles, coin_items, speed, distance, score, coins, game_over, zapper_count, is_speed_boosting, current_tick

    current_tick += 1 # Update global game tick
    
    # --- 1. Calculate Current Speed ---
    speed_boost_gadget = next((g for g in GADGETS if g['name'] == 'Speed Boost'), None)
    
    base_speed_increase = (BASE_SPEED + 0.002 * distance)
    
    if speed_boost_gadget and speed_boost_gadget['purchased'] and is_speed_boosting:
        current_speed = base_speed_increase * speed_boost_gadget['speed_multiplier']
    else:
        current_speed = base_speed_increase
        
    speed = min(current_speed * dt, 15.0) 
    
    # --- 2. Update Player Rect and Center ---
    player_rect = pygame.Rect(PLAYER_START_X, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    player_center_x = PLAYER_START_X + PLAYER_WIDTH // 2
    player_center_y = player_y + PLAYER_HEIGHT // 2

    # --- 3. Apply Coin Magnet Effect (before moving coins) ---
    apply_coin_magnet(dt, player_center_x, player_center_y)

    # --- 4. Move and Check Obstacles (Handling Dynamic Obstacles) ---
    updated_obstacles = []
    for obs in obstacles:
        # Move horizontally
        obs['x'] -= speed 
        
        obs_rect = None
        collision = False

        if obs['type'] == 'top':
            obs_rect = pygame.Rect(obs['x'], 16, 60, obs['height'])
            
        elif obs['type'] == 'bottom':
            y = SCREEN_HEIGHT - 16 - obs['height']
            obs_rect = pygame.Rect(obs['x'], y, 60, obs['height'])
            
        elif obs['type'] == 'floating':
            obs_rect = pygame.Rect(obs['x'], obs['y'], obs['size'], obs['size'])
            
        # --- Dynamic Obstacle Logic ---
        elif obs['type'] == 'moving_block':
            # Vertical movement: use sine wave for smooth up/down motion
            obs['current_y'] = obs['start_y'] + obs['amplitude'] * math.sin(current_tick / obs['speed_factor'])
            obs_rect = pygame.Rect(obs['x'], obs['current_y'], 60, 60)
            
        elif obs['type'] == 'rotating_laser':
            # Rotation: constant angular speed
            obs['angle'] += obs['rotation_speed'] * dt
            obs['angle'] %= 360
            
            center = (obs['x'] + obs['radius'], obs['y'])
            p1, p2 = get_rotated_rect(center, obs['length'], obs['angle'])
            
            # Use the dedicated line collision check
            if check_line_collision(player_rect, p1, p2):
                 collision = True

        # Check for collision 
        if obs_rect and player_rect.colliderect(obs_rect):
            collision = True

        if collision:
            game_over = True
        
        # Check if obstacle is passed (for mission tracking)
        if obs['x'] + 60 < PLAYER_START_X and not obs.get('passed'):
            if obs['type'] in ['floating', 'rotating_laser', 'moving_block']:
                zapper_count += 1
            obs['passed'] = True
            
        if obs['x'] > -200: # Keep dynamic obstacles on screen longer
            updated_obstacles.append(obs)
            
    obstacles = updated_obstacles

    # --- 5. Move Coins (that weren't magnet-pulled/collected) ---
    updated_coins = []
    for coin in coin_items:
        if not coin.get('pulling'):
            coin['x'] -= speed
        
        coin_rect = pygame.Rect(coin['x'], coin['y'], 20, 20)
        
        if player_rect.colliderect(coin_rect):
            coins += 1
            score += 10
            MISSIONS[0]['progress'] = min(MISSIONS[0]['target'], MISSIONS[0]['progress'] + 1)
        elif coin['x'] > -50:
            updated_coins.append(coin)
            
    coin_items = updated_coins

    # --- 6. Update Score/Distance/Missions ---
    distance += 0.1 * dt
    score += 1 * dt
    
    # Update distance mission progress
    MISSIONS[1]['progress'] = math.floor(distance)
    MISSIONS[2]['progress'] = zapper_count
    
    check_missions()


def check_missions():
    global coins
    for mission in MISSIONS:
        if not mission['completed'] and mission['progress'] >= mission['target']:
            mission['completed'] = True
            coins += mission['reward']
            print(f"MISSION COMPLETED: {mission['desc']}! Awarded {mission['reward']} coins.")


def spawn_elements():
    global obstacle_spawn_counter, coin_spawn_counter, obstacles, coin_items
    
    obstacle_spawn_counter -= 1
    if obstacle_spawn_counter <= 0:
        # Adjust spawn rate based on current speed for proper spacing
        dynamic_spawn_rate = max(int(OBSTACLE_SPAWN_RATE / (speed / BASE_SPEED)), FPS // 3) 
        obstacle_spawn_counter = dynamic_spawn_rate
        
        # Increased chance of dynamic obstacles
        obstacle_type_rand = random.random()
        new_obs = {'id': pygame.time.get_ticks(), 'x': SCREEN_WIDTH, 'passed': False}

        if obstacle_type_rand < 0.2: # Standard Top/Bottom blocks less frequent
            height = random.uniform(100, 250)
            new_obs.update({'type': 'top', 'height': height})
        elif obstacle_type_rand < 0.4:
            height = random.uniform(100, 250)
            new_obs.update({'type': 'bottom', 'height': height})
        elif obstacle_type_rand < 0.6: # Standard Zapper
            y = random.uniform(100, 450)
            size = random.uniform(80, 140)
            new_obs.update({'type': 'floating', 'y': y, 'size': size})
        elif obstacle_type_rand < 0.8: # --- New: Moving Block ---
            start_y = random.uniform(100, 400)
            new_obs.update({'type': 'moving_block', 'start_y': start_y, 'current_y': start_y, 'amplitude': random.uniform(50, 150), 'speed_factor': random.uniform(30.0, 60.0)})
        else: # --- New: Rotating Laser ---
            center_y = random.uniform(100, 500)
            new_obs.update({'type': 'rotating_laser', 'y': center_y, 'radius': 10, 'length': random.uniform(100, 250), 'angle': random.uniform(0, 360), 'rotation_speed': random.uniform(3.0, 6.0)})

            
        obstacles.append(new_obs)
        
    coin_spawn_counter -= 1
    if coin_spawn_counter <= 0:
        coin_spawn_counter = COIN_SPAWN_RATE
        y = random.uniform(50, 550)
        new_coin = {'id': pygame.time.get_ticks(), 'x': SCREEN_WIDTH, 'y': y}
        coin_items.append(new_coin)
        

# --- Game State Management ---

def start_game():
    global game_state, player_y, velocity, speed, obstacles, coin_items
    global game_over, distance, score, obstacle_spawn_counter, coin_spawn_counter, zapper_count, current_tick
    
    game_state = 'playing'
    player_y = GROUND_Y
    velocity = 0
    speed = BASE_SPEED
    obstacles = []
    coin_items = []
    game_over = False
    distance = 0
    score = 0
    zapper_count = 0
    current_tick = 0
    obstacle_spawn_counter = OBSTACLE_SPAWN_RATE
    coin_spawn_counter = COIN_SPAWN_RATE
    
    # Reset mission run-specific progress
    MISSIONS[1]['progress'] = 0
    MISSIONS[2]['progress'] = 0


def back_to_menu():
    global game_state, score, high_score
    game_state = 'menu'
    if score > high_score:
        high_score = int(score)


# --- Drawing Functions for Menu Screens (omitted for brevity, assume unchanged) ---
def draw_rounded_panel(surface, rect, color, border_radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)
    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=border_radius)

def draw_menu():
    SCREEN.fill(DARK_BLUE)
    # ... (rest of draw_menu code)
    header_rect = pygame.Rect(40, 50, 300, 500)
    draw_rounded_panel(SCREEN, header_rect, MENU_PANEL)
    coin_icon = font_medium.render("💰", True, YELLOW) 
    coin_text = font_medium.render(f"COINS: {coins}", True, WHITE)
    SCREEN.blit(coin_icon, (header_rect.x + 20, header_rect.y + 20))
    SCREEN.blit(coin_text, (header_rect.x + 60, header_rect.y + 25))
    title_text = font_large.render("JETPACK JOYRIDE", True, YELLOW)
    SCREEN.blit(title_text, (header_rect.centerx - title_text.get_width() // 2, header_rect.y + 100))
    draw_player(SCREEN, header_rect.centerx - PLAYER_WIDTH // 2, header_rect.y + 180, False)
    play_button_rect = pygame.Rect(header_rect.x + 50, 400, 200, 60)
    gadgets_button_rect = pygame.Rect(header_rect.x + 50, 470, 200, 60)
    pygame.draw.rect(SCREEN, BUTTON_GREEN, play_button_rect, border_radius=10)
    pygame.draw.rect(SCREEN, GREEN, gadgets_button_rect, border_radius=10)
    play_text = font_large.render("PLAY", True, BLACK)
    gadgets_text = font_large.render("GADGETS", True, BLACK)
    SCREEN.blit(play_text, (play_button_rect.centerx - play_text.get_width() // 2, play_button_rect.centery - play_text.get_height() // 2))
    SCREEN.blit(gadgets_text, (gadgets_button_rect.centerx - gadgets_text.get_width() // 2, gadgets_button_rect.centery - gadgets_text.get_height() // 2))
    missions_rect = pygame.Rect(370, 50, 400, 280)
    draw_rounded_panel(SCREEN, missions_rect, MENU_PANEL)
    header = font_medium.render("MISSIONS", True, WHITE)
    SCREEN.blit(header, (missions_rect.centerx - header.get_width() // 2, missions_rect.y + 15))
    pygame.draw.line(SCREEN, WHITE, (missions_rect.x + 20, missions_rect.y + 50), (missions_rect.right - 20, missions_rect.y + 50))
    y_offset = missions_rect.y + 70
    for mission in MISSIONS:
        text_color = GREEN if mission['completed'] else WHITE
        progress_text = ""
        if mission['completed']:
            progress_text = "[DONE]"
        elif mission['id'] == 1:
            progress_text = f"({mission['progress']}/{mission['target']})"
        elif mission['id'] == 2:
            progress_text = f"({mission['progress']}/{mission['target']}m)"
        elif mission['id'] == 3:
            progress_text = f"({mission['progress']}/{mission['target']})"

        desc = font_small.render(mission['desc'], True, text_color)
        progress = font_small.render(progress_text, True, YELLOW)
        icon_color = GREEN if mission['completed'] else YELLOW
        pygame.draw.circle(SCREEN, icon_color, (missions_rect.x + 30, y_offset + 10), 8)
        SCREEN.blit(desc, (missions_rect.x + 50, y_offset))
        SCREEN.blit(progress, (missions_rect.right - progress.get_width() - 20, y_offset))
        y_offset += 40
    gadgets_rect = pygame.Rect(370, 350, 400, 200)
    draw_rounded_panel(SCREEN, gadgets_rect, MENU_PANEL)
    header = font_medium.render("GADGETS", True, WHITE)
    SCREEN.blit(header, (gadgets_rect.centerx - header.get_width() // 2, gadgets_rect.y + 15))
    pygame.draw.line(SCREEN, WHITE, (gadgets_rect.x + 20, gadgets_rect.y + 50), (gadgets_rect.right - 20, gadgets_rect.y + 50))
    x_offset = gadgets_rect.x + 40
    gadget_button_rects = []
    for gadget in GADGETS:
        gadget_area = pygame.Rect(x_offset, gadgets_rect.y + 65, 100, 120)
        box_color = BUTTON_GREEN if gadget['purchased'] else (60, 70, 110)
        pygame.draw.rect(SCREEN, box_color, gadget_area, border_radius=5)
        pygame.draw.rect(SCREEN, WHITE, gadget_area, 1, border_radius=5)
        icon_color = YELLOW if gadget['purchased'] else RED
        pygame.draw.circle(SCREEN, icon_color, (x_offset + 50, gadgets_rect.y + 90), 20)
        name_text = font_small.render(gadget['name'].split(' ')[0], True, WHITE)
        status_text = "OWNED" if gadget['purchased'] else f"{gadget['price']}"
        status_color = YELLOW
        status_render = font_small.render(status_text, True, status_color)
        SCREEN.blit(name_text, (x_offset + 50 - name_text.get_width() // 2, gadgets_rect.y + 120))
        SCREEN.blit(status_render, (x_offset + 50 - status_render.get_width() // 2, gadgets_rect.y + 145))
        gadget_button_rects.append(gadget_area)
        x_offset += 120 
    return play_button_rect, gadgets_button_rect, gadget_button_rects

def draw_game_over_screen():
    global score, high_score, distance
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    SCREEN.blit(overlay, (0, 0))
    game_over_text = font_large.render("GAME OVER!", True, RED)
    SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
    score_text = font_medium.render(f"SCORE: {int(score)}", True, WHITE)
    dist_text = font_medium.render(f"DISTANCE: {math.floor(distance)}m", True, WHITE)
    SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    SCREEN.blit(dist_text, (SCREEN_WIDTH // 2 - dist_text.get_width() // 2, 290))
    if score > high_score:
        high_score = int(score)
    retry_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 400, 120, 50)
    menu_rect = pygame.Rect(SCREEN_WIDTH // 2 + 30, 400, 120, 50)
    pygame.draw.rect(SCREEN, GREEN, retry_rect, border_radius=5)
    pygame.draw.rect(SCREEN, (52, 152, 219), menu_rect, border_radius=5)
    retry_text = font_medium.render("RETRY", True, WHITE)
    menu_text = font_medium.render("MENU", True, WHITE)
    SCREEN.blit(retry_text, (retry_rect.centerx - retry_text.get_width() // 2, retry_rect.centery - retry_text.get_height() // 2))
    SCREEN.blit(menu_text, (menu_rect.centerx - menu_text.get_width() // 2, menu_rect.centery - menu_text.get_height() // 2))
    return retry_rect, menu_rect

def draw_gadget_store():
    SCREEN.fill(DARK_BLUE)
    panel_rect = pygame.Rect(50, 50, 700, 500)
    draw_rounded_panel(SCREEN, panel_rect, MENU_PANEL)
    header = font_large.render("CUSTOMIZATION & SHOP", True, YELLOW)
    SCREEN.blit(header, (SCREEN_WIDTH // 2 - header.get_width() // 2, 70))
    coin_text = font_medium.render(f"COINS: {coins}", True, YELLOW)
    SCREEN.blit(coin_text, (550, 75))
    back_rect = pygame.Rect(60, 480, 120, 50)
    pygame.draw.rect(SCREEN, RED, back_rect, border_radius=5)
    back_text = font_medium.render("BACK", True, WHITE)
    SCREEN.blit(back_text, (back_rect.centerx - back_text.get_width() // 2, back_rect.centery - back_text.get_height() // 2))
    y_offset = 150
    gadget_shop_buttons = []
    gadget_header = font_medium.render("GADGETS", True, WHITE)
    SCREEN.blit(gadget_header, (70, y_offset - 30))
    pygame.draw.line(SCREEN, WHITE, (70, y_offset - 5), (680, y_offset - 5))
    for gadget in GADGETS:
        is_purchased = gadget['purchased']
        name_render = font_small.render(gadget['name'], True, WHITE)
        SCREEN.blit(name_render, (70, y_offset))
        button_text = "OWNED" if is_purchased else f"BUY {gadget['price']}"
        button_color = GREEN if is_purchased else YELLOW
        text_color = BLACK
        buy_rect = pygame.Rect(550, y_offset - 10, 120, 30)
        pygame.draw.rect(SCREEN, button_color, buy_rect, border_radius=5)
        buy_text = font_small.render(button_text, True, text_color)
        SCREEN.blit(buy_text, (buy_rect.centerx - buy_text.get_width() // 2, buy_rect.centery - buy_text.get_height() // 2))
        gadget_shop_buttons.append((gadget, buy_rect))
        y_offset += 40
    y_offset += 40
    look_shop_buttons = []
    look_header = font_medium.render("CHARACTER LOOKS", True, WHITE)
    SCREEN.blit(look_header, (70, y_offset - 30))
    pygame.draw.line(SCREEN, WHITE, (70, y_offset - 5), (680, y_offset - 5))
    for look in CHARACTER_LOOKS:
        is_purchased = look['purchased']
        is_active = look['active']
        name_render = font_small.render(look['name'], True, WHITE)
        SCREEN.blit(name_render, (70, y_offset))
        button_text = "ACTIVE" if is_active else ("EQUIP" if is_purchased else f"BUY {look['price']}")
        button_color = (52, 152, 219) if is_active else (GREEN if is_purchased else YELLOW)
        text_color = WHITE if is_active or is_purchased else BLACK
        equip_rect = pygame.Rect(550, y_offset - 10, 120, 30)
        pygame.draw.rect(SCREEN, button_color, equip_rect, border_radius=5)
        equip_text = font_small.render(button_text, True, text_color)
        SCREEN.blit(equip_text, (equip_rect.centerx - equip_text.get_width() // 2, equip_rect.centery - equip_text.get_height() // 2))
        look_shop_buttons.append((look, equip_rect))
        y_offset += 40
    return back_rect, gadget_shop_buttons, look_shop_buttons

def handle_gadget_purchase(gadget, rect, mouse_pos):
    global coins
    if rect.collidepoint(mouse_pos):
        if not gadget['purchased']:
            if coins >= gadget['price']:
                coins -= gadget['price']
                gadget['purchased'] = True
                print(f"Purchased {gadget['name']}!")
            else:
                print("Not enough coins!")
        
def handle_look_action(look, rect, mouse_pos):
    global coins
    if rect.collidepoint(mouse_pos):
        if not look['purchased']:
            if coins >= look['price']:
                coins -= look['price']
                look['purchased'] = True
                print(f"Purchased {look['name']}!")
            else:
                print("Not enough coins!")
        elif not look['active']:
            for l in CHARACTER_LOOKS:
                l['active'] = False
            look['active'] = True
            print(f"Equipped {look['name']}!")
            
# --- Main Game Loop ---
def main():
    global is_thrusting, game_state, coins, is_speed_boosting
    
    running = True
    shop_back_button = None
    gadget_shop_buttons = []
    look_shop_buttons = []
    
    while running:
        dt = clock.tick(FPS) / 60.0 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- Input Handling ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                
                if game_state == 'playing' and not game_over:
                    is_thrusting = True
                    
                elif game_state == 'menu':
                    play_button, gadgets_button, _ = draw_menu() 
                    if play_button.collidepoint(mouse_pos):
                        start_game()
                    elif gadgets_button.collidepoint(mouse_pos):
                        game_state = 'gadgets'
                        
                elif game_state == 'gadgets':
                    if shop_back_button and shop_back_button.collidepoint(mouse_pos):
                        game_state = 'menu'
                        
                    for gadget, rect in gadget_shop_buttons:
                        handle_gadget_purchase(gadget, rect, mouse_pos)
                        
                    for look, rect in look_shop_buttons:
                        handle_look_action(look, rect, mouse_pos)
                                
                elif game_over:
                    retry_button, menu_button = draw_game_over_screen()
                    if retry_button.collidepoint(mouse_pos):
                        start_game()
                    elif menu_button.collidepoint(mouse_pos):
                        back_to_menu()
                        
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if game_state == 'playing':
                    is_thrusting = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_state == 'playing' and not game_over:
                    is_thrusting = True
                
                if (event.key == pygame.K_s or event.key == pygame.K_d) and game_state == 'playing' and not game_over:
                    speed_boost_gadget = next((g for g in GADGETS if g['name'] == 'Speed Boost'), None)
                    if speed_boost_gadget and speed_boost_gadget['purchased']:
                        is_speed_boosting = True
                        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and game_state == 'playing':
                    is_thrusting = False
                
                if (event.key == pygame.K_s or event.key == pygame.K_d) and game_state == 'playing':
                    is_speed_boosting = False


        # Game Logic Update
        if game_state == 'playing' and not game_over:
            update_player(dt)
            update_elements(dt)
            spawn_elements()


        # Drawing
            if game_state == 'playing':
            
                # --- Achtergrondafbeelding Tekenen (Parallax / Scrollend) ---
                if BACKGROUND_IMAGE:
                    # Bereken de verschuiving (een kleine fractie van de afstand om een parallax-effect te creëren)
                    scroll_speed = 40 # Stel de scroll-snelheid in
                    scroll_x = int(distance * scroll_speed) % SCREEN_WIDTH
                    
                    # Teken de eerste instantie
                    SCREEN.blit(BACKGROUND_IMAGE, (SCREEN_WIDTH - scroll_x, 0))
                    # Teken de tweede instantie om naadloos te scrollen
                    SCREEN.blit(BACKGROUND_IMAGE, (-scroll_x, 0))
                else:
                    # Standaard kleur als de afbeelding niet is geladen
                    SCREEN.fill((52, 152, 219))
                # --- Einde Achtergrond Tekenen ---
                
                # De verticale lijnen geven nu een gevoel van beweging

                pygame.draw.rect(SCREEN, GRAY_CEILING, (0, 0, SCREEN_WIDTH, 16))
                pygame.draw.rect(SCREEN, (100, 100, 100), (0, 0, SCREEN_WIDTH, 16), 4)
                pygame.draw.rect(SCREEN, GRAY_FLOOR, (0, SCREEN_HEIGHT - 16, SCREEN_WIDTH, 16))
                pygame.draw.rect(SCREEN, (100, 100, 100), (0, SCREEN_HEIGHT - 16, SCREEN_WIDTH, 16), 4)
                    
                for obs in obstacles:
                    draw_obstacle(SCREEN, obs)
                    
                for coin in coin_items:
                    draw_coin(SCREEN, coin)
                    
                draw_player(SCREEN, PLAYER_START_X, player_y, is_thrusting)
                draw_hud(SCREEN, int(score), coins, distance)

                if distance < 3 and not game_over:
                    instr_text = font_large.render("HOLD MOUSE/SPACE TO FLY!", True, WHITE)
                    instr_bg = pygame.Rect(SCREEN_WIDTH//2 - instr_text.get_width()//2 - 20, 
                                            SCREEN_HEIGHT//2 - instr_text.get_height()//2 - 20, 
                                            instr_text.get_width() + 40, instr_text.get_height() + 40)
                    pygame.draw.rect(SCREEN, BLACK, instr_bg, border_radius=10)
                    SCREEN.blit(instr_text, (SCREEN_WIDTH // 2 - instr_text.get_width() // 2, 
                                            SCREEN_HEIGHT // 2 - instr_text.get_height() // 2))

                if game_over:
                    draw_game_over_screen()
                    
        elif game_state == 'menu':
            play_button, gadgets_button, _ = draw_menu() 
            
        elif game_state == 'gadgets':
            shop_back_button, gadget_shop_buttons, look_shop_buttons = draw_gadget_store()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()