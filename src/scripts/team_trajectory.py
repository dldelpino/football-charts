import pandas as pd

def teams_list(league):
    path = f"public/data/{league.lower().replace(" ", "_")}.csv"
    df = pd.read_csv(path)
    return df["Team"].unique().tolist()

leagues = ["LaLiga", "Premier League", "Serie A", "Bundesliga", "Ligue 1"]

for league in leagues:
    print(f'{league} teams:')
    print(teams_list(league))
    print('')