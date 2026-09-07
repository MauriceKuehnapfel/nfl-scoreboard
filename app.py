import json

from flask import Flask, render_template

app = Flask(__name__)


def load_games():
    with open("games.json", "r") as file:
        return json.load(file)


def get_all_scores():
    games = load_games()
    if not games:
        return []
    scores = []
    for game in games:
        score = (f"\n========== Score Board ==========\n"
                f"{game['home']}\n"
                f"{game['home_score']}\n"
                f"{game['away']}\n"
                f"{game['away_score']}\n"
                f"Status: {game['status']}\n"
                f"start_time: {game['start_time']}\n"
                "\n================================\n"
                "")
        scores.append(score)
    return scores


def display_games(scores):
    if not scores:
        print("No games available")
        return
    
    for score in scores:
        print(score)

@app.route("/")
def home():
    games = load_games()

    return render_template(
        "index.html",
        games=games
    )

def main():
    scores = get_all_scores()
    display_games(scores)

if __name__ == "__main__":
    app.run(debug=True)
