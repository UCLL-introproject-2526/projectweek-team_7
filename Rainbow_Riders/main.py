# main.py
import sys
import random
import pygame
import time

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

# Laadt alle assets (afbeeldingen, geluiden, fonts) met een laadscherm
startup_loading_screen([
    load_images,
    load_audio,
    load_fonts,
])

def main():
    # === GAME STATE ===
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

        # 🔥 Highscore melding
        "new_highscore": False,
        "highscore_time": 0
    }

    running = True
    start_button = None

    # === MAIN GAME LOOP ===
    while running:
        dt = clock.tick(FPS) / 60.0

        # === EVENT HANDLING ===
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
                    retry, menu_btn = draw_game_over(
                        state["highscore"],
                        state["score"],
                        state["coins"]
                    )
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
                    state["game_over"] = False
                    reset_game(state)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    state["thrusting"] = False
                    if not state["game_active"] and not state["game_over"]:
                        start_background_music()
                        state["game_active"] = True
                        state["game_over"] = False
                        reset_game(state)

        # === GAME LOGIC ===
        if state["game_active"] and not state["game_over"]:
            # Speler fysica
            state["player_y"], state["player_vel"] = apply_physics(
                state["player_y"],
                state["player_vel"],
                state["thrusting"]
            )

            # Obstakels spawnen
            state["spawn_timer"] += 1.05
            if state["spawn_timer"] > 60:
                state["obstacles"].append(spawn_obstacle())
                state["spawn_timer"] = 0

            # Munten spawnen
            if random.random() < 0.02:
                state["coin_items"].append(spawn_coin())

            # Beweging
            state["obstacles"] = move_obstacles(state["obstacles"], state["speed"])
            state["coin_items"] = move_coins(state["coin_items"], state["speed"])

            # Munten verzamelen
            gained = check_coin_collect(
                state["player_x"],
                state["player_y"],
                state["coin_items"]
            )
            if gained:
                state["coins"] += gained
                state["score"] += gained * 10

            # Score & snelheid
            state["score"] += 0.1
            state["speed"] = 5 + state["score"] / 150

            # NIEUWE HIGHSCORE CHECK (TIJDENS HET SPELEN)
            if int(state["score"]) > state["highscore"]:
                state["highscore"] = int(state["score"])
                save_highscore(state["highscore"])

                # Slechts 1x per run triggeren
                if not state["new_highscore"]:
                    state["new_highscore"] = True
                    state["highscore_time"] = time.time()

            # Botsing (GEEN highscore-logica meer hier!)
            if check_collision(
                state["player_x"],
                state["player_y"],
                state["obstacles"]
            ):
                state["game_over"] = True

        # === DRAWING ===
        if state["game_active"]:
            draw_background()

            pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 20))
            pygame.draw.rect(screen, GRAY, (0, HEIGHT - 20, WIDTH, 20))

            for obs in state["obstacles"]:
                draw_obstacle(obs)
            for coin in state["coin_items"]:
                draw_coin(coin)

            draw_player(
                state["player_x"],
                state["player_y"],
                state["thrusting"]
            )

            # UI
            screen.blit(
                font_small.render(f"Highscore: {state['highscore']}", True, WHITE),
                (10, 10)
            )
            screen.blit(
                font_small.render(f"Score: {int(state['score'])}", True, WHITE),
                (10, 35)
            )
            screen.blit(
                font_small.render(f"Munten: {state['coins']}", True, YELLOW),
                (10, 60)
            )

            # NEW HIGHSCORE MELDING (5 seconden, ook bij game over)
            if state["new_highscore"] and not state["game_over"]:
                if time.time() - state["highscore_time"] < 5:
                    if int(time.time() * 3) % 2 == 0:
                        text = font_small.render(
                            "NEW HIGHSCORE!",
                            True,
                            (255, 215, 0)
                        )
                        screen.blit(text, (10, 85))

            if state["game_over"]:
                draw_game_over(
                    state["highscore"],
                    state["score"],
                    state["coins"]
                )
        else:
            start_button = draw_menu(state["coins"], PLAYER_W, PLAYER_H)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
