def draw_player_fallback(x, y, thrusting):
    pygame.draw.rect(screen, (139, 69, 19), (x, y, 40, 60), border_radius=5)
    pygame.draw.circle(screen, (255, 200, 150), (x + 20, y - 10), 15)
    pygame.draw.circle(screen, BLACK, (x + 20, y - 10), 8)

    if thrusting:
        flame_y = y + 60
        for i in range(3):
            offset = random.randint(-5, 5)
            pygame.draw.circle(screen, YELLOW, (x + 20 + offset, flame_y + i*5), 8 - i*2)

def draw_player(x, y, thrusting):
    if image_loaded and player_image:
        screen.blit(player_image, (x, y))
        if thrusting:
            flame_y = y + player_h
            for i in range(3):
                offset = random.randint(-5, 5)
                pygame.draw.circle(screen, YELLOW, (x + player_w//2 + offset, flame_y + i*5), 8 - i*2)
                pygame.draw.circle(screen, RED, (x + player_w//2 + offset, flame_y + i*5), 4 - i)
    else:
        draw_player_fallback(x, y, thrusting)
