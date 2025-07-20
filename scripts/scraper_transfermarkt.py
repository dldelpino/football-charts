import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_table(competition, year): # el año 2000 corresponde a la temporada 00/01, y así con todos
    season = f"{str(year)[2:]}/{str(year+1)[2:]}" # la f permite introducir variables dentro de la URL
    if competition == 0: # LaLiga
        url = f"https://www.transfermarkt.es/primera-division/tabelle/wettbewerb/ES1/saison_id/{year}"
    elif competition == 1: # Premier League
        url = f"https://www.transfermarkt.es/premier-league/tabelle/wettbewerb/GB1/saison_id/{year}"
    elif competition == 2: # Serie A
        url = f"https://www.transfermarkt.es/serie-a/tabelle/wettbewerb/IT1/saison_id/{year}" 
    elif competition == 3: # Bundesliga
        url = f"https://www.transfermarkt.es/bundesliga/tabelle/wettbewerb/L1/saison_id/{year}"
    elif competition == 4: # Ligue 1
        url = f"https://www.transfermarkt.es/ligue-1/tabelle/wettbewerb/FR1/saison_id/{year}"
    headers = {
        "User-Agent": "Mozilla/5.0" # si quito esto, algunas webs bloquean la solicitud al detectar que viene de un bot
    }
    response = requests.get(url, headers = headers)
    html = response.content
    soup = BeautifulSoup(html, "lxml") # la segunda variable es el HTML parser
    table = soup.find("table", class_ = "items") # se utiliza class_ en lugar de class para evitar conflictos con Python
    rows = table.find_all("tr")[1:] # el primer tr está en el encabezado
    data = [] # data es una lista cuyos elementos van a ser diccionarios
    for row in rows:
        cols = row.find_all("td")
        position = int(cols[0].text.strip()) # cols[0].text devuelve la posición con dos espacios innecesarios a la derecha, y es un string
        team = cols[2].text.strip()
        if competition == 2: # cosas raras que hace Transfermarkt con los nombres de equipos italianos
            if team == "Nápoles":
                team = "Napoli"
            elif team == "AC Venezia 1907":
                team = "Venezia"
            elif team == "Milan":
                team = "AC Milan"
            elif team == "AC Parma":
                team = "Parma"
        matches = int(cols[3].text.strip())
        wins = int(cols[4].text.strip())
        draws = int(cols[5].text.strip())
        losses = int(cols[6].text.strip())
        goals_for, goals_against = map(int, cols[7].text.strip().split(":"))
        goal_diff = goals_for - goals_against
        points = int(cols[9].text.strip())
        data.append({ # esto es un diccionario
            "Season": season,
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
        })
    return pd.DataFrame(data) # DataFrame es una estructura de datos de pandas que es algo similar a una tabla

laliga = []
premier_league = []
serie_a = []
bundesliga = []
ligue_1 = []

for year in range(2000, 2025):
    season = f"{str(year)[2:]}/{str(year+1)[2:]}"
    print(f"Extrayendo datos de la temporada {season}...")
    try:
        laliga.append(get_table(0, year))
        premier_league.append(get_table(1, year))
        serie_a.append(get_table(2, year))
        bundesliga.append(get_table(3, year))
        ligue_1.append(get_table(4, year))
    except Exception as e:
        print(f"Error en la temporada {season}: {e}")
    # time.sleep(2) # pausa el programa durante 2 segundos para que no la web no dé problemas

laliga_df = pd.concat(laliga, ignore_index = True) # pd.concat une varios DataFrames en uno solo; ignore_index = True reinicia los índices del nuevo DataFrame
laliga_df.to_csv("data/laliga.csv", index = False) # no hace falta guardar los índices del DataFrame

premier_league_df = pd.concat(premier_league, ignore_index = True)
premier_league_df.to_csv("data/premier_league.csv", index = False)

serie_a_df = pd.concat(serie_a, ignore_index = True)
serie_a_df.to_csv("data/serie_a.csv", index = False)

bundesliga_df = pd.concat(bundesliga, ignore_index = True)
bundesliga_df.to_csv("data/bundesliga.csv", index = False)

ligue_1_df = pd.concat(ligue_1, ignore_index = True)
ligue_1_df.to_csv("data/ligue_1.csv", index = False)