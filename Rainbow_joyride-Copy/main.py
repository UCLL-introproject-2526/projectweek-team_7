# main.py
import sys
import random
import pygame
import Startup

from Startup import *
from player_colors import *
from Achtergrond import *
from player import *
from obstacles import *
from coins import *
from hitboxes import *
from menu import *
from states import *
from audio import *
from load_highscore import *
import time

Startup.startup_loading_screen([
    load_images,
    load_audio,
    load_fonts,
])

def check_collision(px, py, obstacles):
    p = player_rect(px, py)
    for obs in obstacles:
        if obs["type"] == "laser":
            if check_laser_collision(px, py, obs):
                return True
        else:
            # Normale collision voor andere obstakels
            if p.colliderect(obstacle_rect(obs)):
                game_over_sound()
                return True
    return False

def check_coin_collect(px, py, coin_items):
    p = pygame.Rect(px, py, PLAYER_W, PLAYER_H)
    collected = 0
    to_remove = []
    for coin in coin_items:
        if p.colliderect(coin_rect(coin)):
            coin_collect_sound()
            collected += 1
            to_remove.append(coin)
    for c in to_remove:
        coin_items.remove(c)
    return collected




def main():
    # Game variables/state
    state = {
        "WIDTH": WIDTH,
        "HEIGHT": HEIGHT,

        "player_x": 100,
        "player_y": HEIGHT - 150,
        "player_vel": 0,

        "game_active": False,
        "game_over": False,
        "thrusting": False,
        "highscore": load_highscore(),
        "score": 0.0,
        "coins": 0,
        "speed": 4.0,

        "obstacles": [],
        "coin_items": [],
        "spawn_timer": 0,
        "new_highscore": False,  
        "highscore_shown": False,
        "highscore_time": 0
    }

    running = True
    start_button = None

    while running:
        dt = clock.tick(FPS) / 60.0

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if not state["game_active"]:
                    if start_button and start_button.collidepoint(mouse_pos):
                        start_background_music()
                        state["game_active"] = True
                        state["game_over"] = False
                        reset_game(state)

                elif state["game_active"] and not state["game_over"]:
                    state["thrusting"] = True

                elif state["game_over"]:
                    stop_background_music()
                    retry, menu_btn = draw_game_over(state["score"], state["coins"])
                    if retry.collidepoint(mouse_pos):
                        start_background_music()
                        state["game_over"] = False
                        reset_game(state)
                    elif menu_btn.collidepoint(mouse_pos):
                        state["game_active"] = False
                        state["game_over"] = False

            if event.type == pygame.MOUSEBUTTONUP:
                state["thrusting"] = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and state["game_active"] and not state["game_over"]:
                    state["thrusting"] = True

                elif event.key == pygame.K_SPACE and state["game_over"]:
                    start_background_music()
                    state["game_over"] = False
                    reset_game(state)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    state["thrusting"] = False

            

        # Game logic
        if state["game_active"] and not state["game_over"]:
            state["player_y"], state["player_vel"] = apply_physics(
                state["player_y"], state["player_vel"], state["thrusting"]
            )

            # Spawn obstacles + coins
            state["spawn_timer"] += 1
            if state["spawn_timer"] > 60:
                state["obstacles"].append(spawn_obstacle())
                state["spawn_timer"] = 0

            if random.random() < 0.02:
                state["coin_items"].append(spawn_coin())

            # Move
            state["obstacles"] = move_obstacles(state["obstacles"], state["speed"])
            state["coin_items"] = move_coins(state["coin_items"], state["speed"])

            
            # Collisions
            if check_collision(state["player_x"], state["player_y"], state["obstacles"]):
                state["game_over"] = True

            if int(state["score"]) > state["highscore"]:
                if not state["new_highscore"]:  # <-- Alleen de eerste keer
                    state["new_highscore"] = True
                    state["highscore_time"] = time.time()  # <-- NIEUW: sla tijd op
                state["highscore"] = int(state["score"])
                save_highscore(state["highscore"])

            gained = check_coin_collect(state["player_x"], state["player_y"], state["coin_items"])
            if gained:
                state["coins"] += gained
                state["score"] += gained * 10

            # Score + speed
            state["score"] += 0.1
            state["speed"] = min(5 + state["score"] / 200, 10)

        # Drawing
        if state["game_active"]:
            draw_background()

            # Top + bottom bars
            pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 20))
            pygame.draw.rect(screen, GRAY, (0, HEIGHT - 20, WIDTH, 20))

            # Objects
            for obs in state["obstacles"]:
                draw_obstacle(obs)
            for coin in state["coin_items"]:
                draw_coin(coin)

            draw_player(state["player_x"], state["player_y"], state["thrusting"])

            score_text = font_small.render(f"Score: {int(state['score'])}", True, WHITE)
            coin_text = font_small.render(f"Munten: {state['coins']}", True, YELLOW)
            highscore_text = font_small.render(f"Highscore: {state['highscore']}", True, WHITE)
            screen.blit(highscore_text, (10, 10))
            screen.blit(score_text, (10, 35))
            screen.blit(coin_text, (10, 60))


            if state["new_highscore"] and not state["game_over"]:
                # Check of er minder dan 5 seconden verstreken zijn
                if time.time() - state["highscore_time"] < 5:  # <-- NIEUW
                    # Knipperend effect
                    if int(time.time() * 3) % 2 == 0:  # Knippert 3x per seconde
                        new_hs_text = font_small.render("NEW HIGHSCORE!", True, (255, 215, 0))
                        screen.blit(new_hs_text, (10, 85))

            if state["game_over"]:
                draw_game_over(state["score"], state["coins"])
        else:
            start_button = draw_menu(state["coins"], PLAYER_W, PLAYER_H)


        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()