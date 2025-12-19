
def load_highscore():
    try:
        with open("Rainbow_Riders\\highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0


def save_highscore(score):
    with open("Rainbow_Riders\\highscore.txt", "w") as f:
        f.write(str(score))
