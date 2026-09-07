import os

import requests

from dotenv import load_dotenv

import json

from pathlib import Path

load_dotenv()

url = "https://v1.american-football.api-sports.io/games"

headers = {
    "x-apisports-key": os.environ["API_SPORTS_KEY"]
}

try:
    response = requests.get(
        url,
        headers=headers,
        params={"league": 1, "season": 2024},
        timeout=10
    )
    response.raise_for_status()

    data = response.json()

    if data.get("errors"):
        print("API error:", data["errors"])
    else:
        games = []

        for item in data.get("response", []):
            if (
                item["game"]["stage"] != "Regular Season"
                or item["game"]["week"] != "Week 1"
            ):
                continue
            game = {
                "home": item["teams"]["home"]["name"],
                "away": item["teams"]["away"]["name"],
                "home_score": item["scores"]["home"]["total"],
                "away_score": item["scores"]["away"]["total"],
                "status": item["game"]["status"]["long"],
                "start_time": (
                    f"{item['game']['date']['date']} "
                    f"{item['game']['date']['time']} UTC"
                )
            }

            games.append(game)

        if games:
            file_path = Path(__file__).with_name("games.json")

            with file_path.open("w", encoding="utf-8") as file:
                json.dump(games, file, indent=4)

            print(f"Saved {len(games)} games to games.json")

        for game in games[:3]:
            print(game)

except requests.RequestException as error:
    print("Request failed:", error)