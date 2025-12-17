
def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        # Als bestand niet bestaat of fout is
        return 0


def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))
