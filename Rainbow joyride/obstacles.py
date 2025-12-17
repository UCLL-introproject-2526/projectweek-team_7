obstacles = []

def spawn_obstacle():
    obs_type = random.choice(['top', 'bottom', 'float'])
    if obs_type == 'top':
        return {'type': 'top', 'x': WIDTH, 'h': random.randint(100, 250)}
    elif obs_type == 'bottom':
        return {'type': 'bottom', 'x': WIDTH, 'h': random.randint(100, 250)}
    else:
        return {'type': 'float', 'x': WIDTH, 'y': random.randint(100, HEIGHT-150), 's': random.randint(60, 100)}

def draw_obstacle(obs):
    if obs['type'] == 'top':
        pygame.draw.rect(screen, RED, (obs['x'], 0, 50, obs['h']))
    elif obs['type'] == 'bottom':
        pygame.draw.rect(screen, RED, (obs['x'], HEIGHT - obs['h'], 50, obs['h']))
    else:
        pygame.draw.rect(screen, (128, 0, 128), (obs['x'], obs['y'], obs['s'], obs['s']))
