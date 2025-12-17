coin_items = []
coins = 0

def spawn_coin():
    return {'x': WIDTH, 'y': random.randint(50, HEIGHT-100)}

def draw_coin(coin):
    pygame.draw.circle(screen, YELLOW, (coin['x'], coin['y']), 12)
    pygame.draw.circle(screen, (200, 150, 0), (coin['x'], coin['y']), 10)
    text = font_small.render("$", True, BLACK)
    screen.blit(text, (coin['x']-6, coin['y']-10))
