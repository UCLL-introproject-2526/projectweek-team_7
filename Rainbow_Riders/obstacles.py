import random
import pygame
import math

from Startup import WIDTH, HEIGHT, screen
from player_colors import RED, YELLOW, PURPLE

# Laad de afbeelding voor floating obstacles
# Zorg dat je een afbeelding hebt in je project map (bijv. 'float_obstacle.png')
try:
    float_image = pygame.image.load("Rainbow_Riders\\Background\\background\\mimic_chest.png")
    # Je kunt de afbeelding schalen naar de gewenste grootte
    # float_image = pygame.transform.scale(float_image, (100, 100))
except pygame.error:
    # Als afbeelding niet gevonden wordt, gebruik None en teken een rechthoek
    float_image = None
    print("Warning: 'float_obstacle.png' niet gevonden, gebruik fallback rechthoeken")

def spawn_obstacle():
    obs_type = random.choice(
        ["rainbow", "rainbow", "rainbow", "laser", "float"]
    )

    if obs_type == "rainbow":
        position = random.choice(["top", "bottom"])
        return {
            "type": "rainbow",
            "x": WIDTH,
            "h": random.randint(200, 350),
            "position": position
        }

    elif obs_type == "float":
        return {
            "type": "float",
            "x": WIDTH,
            "y": random.randint(200, HEIGHT - 150),
            "s": random.randint(100, 150)
        }

    else:  # laser
        return {
            "type": "laser",
            "x": WIDTH,
            "y": random.randint(100, HEIGHT - 150),
            "angle": 0,
            "length": 170,
            "rotation_speed": random.choice([3, -3, 4, -4])
        }

    

def draw_obstacle(obs):
    if obs["type"] == "float":
        if float_image is not None:
            # Gebruik de afbeelding
            # Schaal de afbeelding naar de grootte van het obstacle
            scaled_image = pygame.transform.scale(float_image, (obs["s"], obs["s"]))
            screen.blit(scaled_image, (obs["x"], obs["y"]))
        else:
            # Fallback naar de originele rechthoeken als afbeelding niet beschikbaar is
            pygame.draw.rect(screen, PURPLE, (obs["x"], obs["y"], obs["s"], obs["s"]))
            pygame.draw.rect(screen, YELLOW, (obs["x"] + 5, obs["y"] + 5, obs["s"] - 10, obs["s"] - 10), 2)
            
    elif obs["type"] == "laser": 
        # Centrum van de laser
        center_x = obs["x"] + 25
        center_y = obs["y"]
        pygame.draw.circle(screen, (0, 0, 0), (int(center_x), int(center_y)), 15)
        
        # Bereken eindpunt van de laser
        rad = math.radians(obs["angle"])
        end_x = center_x + math.cos(rad) * obs["length"]
        end_y = center_y + math.sin(rad) * obs["length"]
        
        # Teken laser straal
        pygame.draw.line(screen, (0, 170, 255), (center_x, center_y), (end_x, end_y), 5)
        pygame.draw.line(screen, (0, 170, 255), (center_x, center_y), (end_x, end_y), 2)
        obs["angle"] += obs["rotation_speed"]

    else:  # rainbow type
        # Bepaal of rainbow van boven of onder komt
        if obs["position"] == "top":
            start_y = 0
        else:
            start_y = HEIGHT - obs["h"]
        
        # Center positie van de rainbow (midden van de 70px breedte)
        center_x = obs["x"] + 35
        
        colors = [
            (186, 85, 211),   # Paars/violet (binnenste)
            (220, 20, 60),    # Rood
            (255, 140, 0),    # Oranje
            (255, 215, 0),    # Geel
            (32, 178, 170),   # Teal/petrol
            (255, 99, 71),    # Koraalrood
            (70, 130, 180)    # Staalblauw (buitenste)
        ]
        num_arcs = 7
        rainbow_width = 70  # Zelfde breedte als top/bottom obstacles
    
        arc_thickness = rainbow_width // (num_arcs * 2)
        
        for i in range(num_arcs - 1, -1, -1):  # Van buiten naar binnen tekenen
            inner_width = (i + 1) * arc_thickness * 2
            color = colors[i % len(colors)]
            
            if obs["position"] == "top":
                # Rainbow hangt van boven
                # Bereken posities
                left_x = center_x - inner_width // 2
                right_x = center_x + inner_width // 2
                top_y = start_y + obs["h"] - inner_width // 2
                bottom_y = start_y + obs["h"]
                
                # Teken linker rechthoek (verticale lijn naar boven)
                pygame.draw.rect(screen, color, 
                                (left_x, start_y, arc_thickness, obs["h"]))
                
                # Teken rechter rechthoek (verticale lijn naar boven)
                pygame.draw.rect(screen, color, 
                                (right_x - arc_thickness, start_y, arc_thickness, obs["h"]))
                
                # Teken halve cirkel onderaan (omgekeerd)
                rect = pygame.Rect(left_x, top_y, inner_width, inner_width)
                pygame.draw.arc(screen, color, rect, math.pi, 2 * math.pi, arc_thickness)
                
                # Teken zwarte randen
                pygame.draw.line(screen, (0, 0, 0), 
                                (left_x, start_y), (left_x, bottom_y), 1)
                pygame.draw.line(screen, (0, 0, 0), 
                                (right_x, start_y), (right_x, bottom_y), 1)
                pygame.draw.arc(screen, (0, 0, 0), rect, math.pi, 2 * math.pi, 1)
            else:
                # Rainbow staat op de grond
                # Bereken posities
                left_x = center_x - inner_width // 2
                right_x = center_x + inner_width // 2
                top_y = start_y - inner_width // 2
                bottom_y = start_y + obs["h"]
                
                # Teken linker rechthoek (verticale lijn naar beneden)
                pygame.draw.rect(screen, color, 
                                (left_x, start_y, arc_thickness, obs["h"]))
                
                # Teken rechter rechthoek (verticale lijn naar beneden)
                pygame.draw.rect(screen, color, 
                                (right_x - arc_thickness, start_y, arc_thickness, obs["h"]))
                
                # Teken halve cirkel bovenaan
                rect = pygame.Rect(left_x, top_y, inner_width, inner_width)
                pygame.draw.arc(screen, color, rect, 0, math.pi, arc_thickness)
                
                # Teken zwarte randen
                pygame.draw.line(screen, (0, 0, 0), 
                                (left_x, start_y), (left_x, bottom_y), 1)
                pygame.draw.line(screen, (0, 0, 0), 
                                (right_x, start_y), (right_x, bottom_y), 1)
                pygame.draw.arc(screen, (0, 0, 0), rect, 0, math.pi, 1)

def move_obstacles(obstacles, speed):
    for obs in obstacles:
        obs["x"] -= speed
    return [o for o in obstacles if o["x"] > -100]