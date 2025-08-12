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
        relegated_teams = {}
        for i in range(len(seasons)):
            if i < len(seasons) - 1:
                season0 = seasons[i]
                season1 = seasons[i+1]
                teams0 = df[df["Season"] == season0]["Team"].to_list()
                teams1 = df[df["Season"] == season1]["Team"].to_list()
                for team in teams0:
                    if team not in teams1:
                        if team not in relegated_teams.keys():
                            relegated_teams[team] = 1
                        else:
                            relegated_teams[team] += 1
            else:
                if competition == "LaLiga":
                    teams = ["Leganés", "Las Palmas", "Valladolid"]
                elif competition == "Premier League":
                    teams = ["Leicester City", "Ipswich Town", "Southampton"]
                elif competition == "Serie A":
                    teams = ["Empoli", "Venezia", "Monza"]
                elif competition == "Bundesliga":
                    teams = ["Holstein Kiel", "Bochum"]
                elif competition == "Ligue 1":
                    teams = ["Reims", "Saint-Étienne", "Montpellier"]
                for team in teams:
                    if team not in relegated_teams.keys():
                        relegated_teams[team] = 1
                    else:
                        relegated_teams[team] += 1

        relegated_teams = sorted(relegated_teams.items(), key = lambda item: item[1], reverse = True)
        n = relegated_teams[0][1]

        data = []
        for (team, count) in relegated_teams:
            data.append(
                {
                    'name': f'<div class="flex no-wrap gap-2 items-center">{team}<img src="https://raw.githubusercontent.com/dldelpino/football-charts/refs/heads/main/icons/teams/{competition}/{team}.png" class="w-4"></div>',
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
                'name': 'Times relegated',
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