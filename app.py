import json

import os

from flask import Flask, render_template, request, redirect, url_for, session
# Initialize the Flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"] # Set the secret key for session management

def load_games():
    with open("games.json", "r") as file:
        return json.load(file)

# Function to load games from the JSON file
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

# Functions for loading and displaying game scores
def display_games(scores):
    if not scores:
        print("No games available")
        return
    
    for score in scores:
        print(score)
# Route for the home page
@app.route("/")
def home():
    games = load_games()
    favorite_teams = session.get("favorite_teams", [])

    return render_template(
        "index.html",
        games=games,
        favorite_teams=favorite_teams
    )
# Route to handle setting and unsetting the favorite team
@app.route("/favorite", methods=["POST"])
def favorite():
    team = request.form.get("team")

    valid_teams = {
        team_name
        for game in load_games()
        for team_name in (game["home"], game["away"])
    }

    if team not in valid_teams:
        return redirect(url_for("home"))

    favorite_teams = session.get("favorite_teams", [])

    if team in favorite_teams:
        favorite_teams.remove(team)
    else:
        favorite_teams.append(team)

    session["favorite_teams"] = favorite_teams
    session.permanent = True

    return redirect(url_for("home"))

def main():
    scores = get_all_scores()
    display_games(scores)

# Route for displaying favorite teams and their games
@app.route("/favorites")
def favorites():
    favorite_teams = session.get("favorite_teams", [])

    games = [
        game
        for game in load_games()
        if game["home"] in favorite_teams
        or game["away"] in favorite_teams
    ]

    return render_template(
        "favorites.html",
        favorite_teams=favorite_teams,
        games=games
    )

if __name__ == "__main__":
    app.run(debug=True)
