def draw_menu():
    if bg_loaded:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BLUE)

    title = font.render("RAINBOW RIDERS", True, YELLOW)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

    draw_player(WIDTH//2 - player_w//2, 200, False)

    button = pygame.Rect(WIDTH//2 - 100, 400, 200, 60)
    pygame.draw.rect(screen, GREEN, button, border_radius=10)

    text = font.render("START", True, WHITE)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 415))
    return button
