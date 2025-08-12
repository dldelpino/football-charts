from nicegui import ui, app
import pandas as pd

def render():
    chart = None

    def show_results():
        nonlocal chart
        if chart:
            chart.delete()
        competition = competition_select.value
        path = f"data/{competition.lower().replace(" ", "_")}.csv"
        df = pd.read_csv(path)

        seasons = df["Season"].unique().tolist()
        for i in range(len(seasons)):
            if i == 0:
                season1 = seasons[i]
                if competition == "LaLiga":
                    promoted_teams = {
                        "Villarreal": 1, 
                        "Las Palmas": 1, 
                        "Osasuna": 1
                    } # equipos recién ascendidos en la 00/01
                elif competition == "Premier League":
                    promoted_teams = {
                        "Ipswich Town": 1, 
                        "Charlton Ath": 1, 
                        "Manchester City": 1
                    }
                elif competition == "Serie A":
                    promoted_teams = {
                        "Atalanta": 1,
                        "Vicenza": 1, 
                        "Napoli": 1
                    }
                elif competition == "Bundesliga":
                    promoted_teams = {
                        "Köln": 1, 
                        "Energie Cottbus": 1, 
                        "Bochum": 1
                    }
                elif competition == "Ligue 1":
                    promoted_teams = {
                        "Lille": 1, 
                        "Guingamp": 1, 
                        "Toulouse": 1
                    }
            else:
                season0 = seasons[i-1]
                season1 = seasons[i]
                teams0 = df[df["Season"] == season0]["Team"].to_list()
                teams1 = df[df["Season"] == season1]["Team"].to_list()
                for team in teams1:
                    if team not in teams0:
                        if team not in promoted_teams.keys():
                            promoted_teams[team] = 1
                        else:
                            promoted_teams[team] += 1

        promoted_teams = sorted(promoted_teams.items(), key = lambda item: item[1], reverse = True)
        n = promoted_teams[0][1]

        data = []
        for (team, count) in promoted_teams:
            data.append(
                {
                    'name': f'<div class="flex no-wrap gap-2 items-center">{team}<img src="/icons/teams/{competition}/{team}.png" class="w-4"></div>',
                    'y': count,
                    'color': f'hsl(120, 100%, {(1-count/(n+1))*100}%)'
                }
            )
        
        options = { # véase https://www.highcharts.com/demo/highcharts/pie-chart y https://nicegui.io/documentation/highchart
            'title': False,
            'chart': {
                'backgroundColor': 'whitesmoke',
                'type': 'bar',
                'height': 1200,
                'width': 800,
                'marginRight': 20
            },
            'legend': {
                'enabled': False
            },
            'xAxis': {
                'type': 'category',
                'labels': {
                    'useHTML': True,
                    'distance': 25
                }
            },
            'yAxis': {
                'max': n,
                'title': '',
                'labels': {
                    'overflow': 'allow'
                }
            },
            'plotOptions': {
                'bar': {
                    'dataLabels': {
                        'enabled': True,
                        'overflow': 'allow',
                        'crop': False
                    }
                }
            },
            'series': [{
                'name': 'Times promoted',
                'data': data
            }],
            'credits': {'enabled': False}, # elimina la marca de agua
        }

        # al pulsar el botón por primera vez, las etiquetas no se muestran correctamente
        # para arreglar esto, la primera vez que pulse el botón cargo dos gráficos con los mismos datos, oculto el primero y muestro el segundo
        if chart == None: 
            chart = ui.highchart(options)
            chart.visible = False
        
        with container:
            chart = ui.highchart(options)

    competitions = ["LaLiga", "Premier League", "Serie A", "Bundesliga", "Ligue 1"]

    with ui.row():
        competition_select = ui.select(options = competitions, with_input = True).props('outlined bg-color="white" dense color="green-10"').classes("w-[200px]")
        ui.button("Show results", on_click = show_results).props('outline color="green-10"').classes("h-[40px]")

    container = ui.row()