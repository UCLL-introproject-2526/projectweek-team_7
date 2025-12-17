# states.py

def reset_game(state):
    state["player_y"] = state["HEIGHT"] - 150
    state["player_vel"] = 0
    state["score"] = 0
    state["speed"] = 5
    state["obstacles"].clear()
    state["coin_items"].clear()
    state["spawn_timer"] = 0
