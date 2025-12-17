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
    for coin in coin_items[:]:
        coin_rect = pygame.Rect(coin['x']-12, coin['y']-12, 24, 24)
        if player_rect.colliderect(coin_rect):
            coins += 1
            score += 10
            coin_items.remove(coin)
