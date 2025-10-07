import pandas as pd
import json

competitions = ["bundesliga", "laliga", "ligue_1", "premier_league", "serie_a"]
for competition in competitions:
    df = pd.read_csv(f"src/data/{competition}.csv")
    json_data = df.to_json(orient="records")
    with open(f"public/data/{competition}.json", "w", encoding="utf-8") as file:
        file.write(json_data)