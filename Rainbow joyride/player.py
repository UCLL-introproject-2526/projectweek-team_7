WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
GRAY = (80, 80, 80)

# Player stats
player_x = 100
player_y = HEIGHT - 150
player_w, player_h = 60, 80
player_vel = 0

GRAVITY = 0.8
THRUST = -12

# Player image
try:
    player_image = pygame.image.load("C:\\school\\projectweek\\small_game\\avatar_zonder_vlam.png")
    player_image = pygame.transform.scale(player_image, (60, 80))
    image_loaded = True
except:
    player_image = None
    image_loaded = False
