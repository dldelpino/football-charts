import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_table(competition, year): # el año 2000 corresponde a la temporada 00/01, y así con todos
    season_short = f"{str(year)[2:]}/{str(year+1)[2:]}" # 2000 -> 00/01
    season = f"{str(year)}-{str(year+1)}" # 2000 -> 2000-2001
    if competition == 0: # LaLiga
        competition_id = 12
    elif competition == 1: # Premier League
        competition_id = 9
    elif competition == 2: # Serie A
        competition_id = 11
    elif competition == 3: # Bundesliga
        competition_id = 20
    elif competition == 4: # Ligue 1
        competition_id = 13
    url = f"https://fbref.com/en/comps/{competition_id}/{season}"
    headers = {
        "User-Agent": "Mozilla/5.0" # si quito esto, algunas webs bloquean la solicitud al detectar que viene de un bot
    }
    response = requests.get(url, headers = headers)
    print(response)
    html = response.content
    soup = BeautifulSoup(html, "lxml") # la segunda variable es el HTML parser
    table = soup.find("table", id = f"results{season}{competition_id}1_overall")
    rows = table.find_all("tr")[1:] # el primer tr está en el encabezado
    data = [] # data es una lista cuyos elementos van a ser diccionarios
    for i in range(len(rows)):
        cols = rows[i].find_all("td")
        position = i+1
        team = cols[0].text.strip()
        if team == "La Coruña": # nombres extraños que pone FBref
            team == "Deportivo"
        if team == "Racing Sant":
            team = "Racing"
        if team == "Paris S-G":
            team = "PSG"
        matches = int(cols[1].text.strip())
        wins = int(cols[2].text.strip())
        draws = int(cols[3].text.strip())
        losses = int(cols[4].text.strip())
        goals_for = int(cols[5].text.strip())
        goals_against = int(cols[6].text.strip())
        goal_diff = cols[7].text.strip()
        points = int(cols[8].text.strip())
        if year < 2017:
            k = 11
        else:
            k = 15
        top_scorer = cols[k].find("a").text.strip()
        top_scorer_goals = int(cols[k].find("span").text.strip())
        data.append({ # esto es un diccionario
            "Season": season_short,
            "#": position,
            "Team": team,
            "Points": points,
            "MP": matches,
            "W": wins,
            "D": draws,
            "L": losses,
            "GF": goals_for,
            "GA": goals_against,
            "GD": goal_diff,
            "Top Scorer": top_scorer,
            "Top Scorer Goals": top_scorer_goals,
        })
    return pd.DataFrame(data) # DataFrame es una estructura de datos de pandas que es algo similar a una tabla

laliga = []
premier_league = []
serie_a = []
bundesliga = []
ligue_1 = []

for year in range(2023, 2025): # si scrapeo más de tres temporadas en la misma ejecución del script, FBref da error
    season = f"{str(year)[2:]}/{str(year+1)[2:]}"
    print(f"Extrayendo datos de la temporada {season}...")
    try:
        laliga.append(get_table(0, year))
        time.sleep(3) # pausa la ejecución durante 3 segundos para no alcanzar el límite de número de peticiones de FBREF
        premier_league.append(get_table(1, year))
        time.sleep(3)
        serie_a.append(get_table(2, year))
        time.sleep(3)
        bundesliga.append(get_table(3, year))
        time.sleep(3)
        ligue_1.append(get_table(4, year))
    except Exception as e:
        print(f"Error en la temporada {season}: {e}")

laliga_df = pd.concat(laliga, ignore_index = True) # pd.concat une varios DataFrames en uno solo; ignore_index = True reinicia los índices del nuevo DataFrame
# laliga_df.to_csv("data1/laliga.csv", index = False) # utilizar esto para la primera escritura en los archivos CSV
laliga_df.to_csv("data1/laliga.csv", index = False, mode = 'a', header = False) # utilizar esto para las demás escrituras en los archivos CSV

premier_league_df = pd.concat(premier_league, ignore_index = True)
# premier_league_df.to_csv("data1/premier_league.csv", index = False)
premier_league_df.to_csv("data1/premier_league.csv", index = False, mode = 'a', header = False)

serie_a_df = pd.concat(serie_a, ignore_index = True)
# serie_a_df.to_csv("data1/serie_a.csv", index = False)
serie_a_df.to_csv("data1/serie_a.csv", index = False, mode = 'a', header = False)

bundesliga_df = pd.concat(bundesliga, ignore_index = True)
# bundesliga_df.to_csv("data1/bundesliga.csv", index = False)
bundesliga_df.to_csv("data1/bundesliga.csv", index = False, mode = 'a', header = False)

ligue_1_df = pd.concat(ligue_1, ignore_index = True)
# ligue_1_df.to_csv("data1/ligue_1.csv", index = False)
ligue_1_df.to_csv("data1/ligue_1.csv", index = False, mode = 'a', header = False)