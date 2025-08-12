from nicegui import ui, app
import pandas as pd

def render():
    chart = None
    def set_max(e):
        position_select.set_value(1)
        if e.value == "Bundesliga":
            k = 18
        else:
            k = 20
        position_select._props["max"] = k
        position_select.update()

    def show_results():
        nonlocal chart
        if chart:
            chart.delete()
        competition = competition_select.value
        position = position_select.value
        path = f"data/{competition.lower().replace(" ", "_")}.csv"
        df = pd.read_csv(path)
        df = df[df["#"] == position]

        n = len(df["Team"].unique())
        colors = [f'hsl(120, 100%, {p}%)' for p in [int(i/(n+1)*100) for i in range(1, n+1)]]

        if position == 1:
            position_ordinal = 'st'
        elif position == 2:
            position_ordinal = 'nd'
        elif position == 3:
            position_ordinal = 'rd'
        else:
            position_ordinal = 'th'
        series_name = f'Times finished {int(position)}{position_ordinal}'

        data = [{'name': team, 'y': count} for team, count in df["Team"].value_counts().items()]
        
        options = { # véase https://www.highcharts.com/demo/highcharts/pie-chart y https://nicegui.io/documentation/highchart
            'title': False,
            'chart': {
                'backgroundColor': 'whitesmoke',
                'type': 'pie',
                'height': 700,
                'width': 1000
            },
            'colors': colors,
            'plotOptions': {
                'pie': {
                    'size': 500,
                    'dataLabels': {
                        'enabled': True,
                        'useHTML': True,
                        'format': (f'<div class="flex no-wrap gap-2 items-center"><img src="https://raw.githubusercontent.com/dldelpino/football-charts/refs/heads/main/icons/teams/{competition}/{{point.name}}.png" class="w-4">{{point.name}} ({{point.y}}) &#8203 &#8203 &#8203 &#8203 &#8203</div>') # &#8203 añade espacio en blanco
                    }
                }
            },
            'series': [{
                'name': series_name,
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
        competition_select = ui.select(options = competitions, with_input = True, on_change = set_max).props('outlined bg-color="white" dense color="green-10"').classes("w-[200px]")
        position_select = ui.number(value = 1, min = 1, max = 20).props('outlined bg-color="white" dense color="green-10"')
        ui.button("Show results", on_click = show_results).props('outline color="green-10"').classes("h-[40px]")

    container = ui.row()