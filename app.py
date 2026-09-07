import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

BASE_DIR = Path(__file__).resolve().parent


# Load saved games
def load_games():
    with (BASE_DIR / "games.json").open("r", encoding="utf-8") as file:
        return json.load(file)


# Display all teams' games for the selected week
@app.route("/")
def home():
    all_games = load_games()
    favorite_teams = session.get("favorite_teams", [])

    weeks = sorted(
        {game["week"] for game in all_games},
        key=lambda week: int(week.split()[-1])
    )

    selected_week = request.args.get("week", "Week 1")

    if weeks and selected_week not in weeks:
        selected_week = weeks[0]

    games = [
        game
        for game in all_games
        if game["week"] == selected_week
    ]

    return render_template(
        "index.html",
        games=games,
        favorite_teams=favorite_teams,
        weeks=weeks,
        selected_week=selected_week
    )


# Display favourite teams' games for the selected week
@app.route("/favorites")
def favorites():
    all_games = load_games()
    favorite_teams = session.get("favorite_teams", [])

    weeks = sorted(
        {game["week"] for game in all_games},
        key=lambda week: int(week.split()[-1])
    )

    selected_week = request.args.get("week", "Week 1")

    if weeks and selected_week not in weeks:
        selected_week = weeks[0]

    games = [
        game
        for game in all_games
        if game["week"] == selected_week
        and (
            game["home"] in favorite_teams
            or game["away"] in favorite_teams
        )
    ]

    return render_template(
        "favorites.html",
        games=games,
        favorite_teams=favorite_teams,
        weeks=weeks,
        selected_week=selected_week
    )


# Add or remove a favourite team when a star is clicked
@app.route("/favorite", methods=["POST"])
def favorite():
    team = request.form.get("team")
    page = request.form.get("page", "home")
    week = request.form.get("week", "Week 1")

    # Only allow redirects to our two scoreboard pages.
    if page not in ("home", "favorites"):
        page = "home"

    valid_teams = {
        team_name
        for game in load_games()
        for team_name in (game["home"], game["away"])
    }

    if team in valid_teams:
        favorite_teams = session.get("favorite_teams", [])

        if team in favorite_teams:
            favorite_teams.remove(team)
        else:
            favorite_teams.append(team)

        session["favorite_teams"] = favorite_teams
        session.permanent = True

    return redirect(url_for(page, week=week))


if __name__ == "__main__":
    app.run(debug=True)