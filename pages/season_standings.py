from nicegui import ui
import pandas as pd

def render():
    def show_results():
        competition = competition_select.value
        season = season_select.value
        path = f"data/{competition.lower().replace(" ", "_")}.csv"
        df = pd.read_csv(path)
        filtered_df = df[df["Season"] == season]
        cols = []
        for col in filtered_df.columns:
            if col == "Team":
                cols.append({'name': col, 'label': col, 'field': col, 'sortable': True, 'align': 'left'})
            elif col == "Points":
                cols.append({'name': col, 'label': col, 'field': col, 'sortable': True, 'style': 'font-weight: bold'})
            else:
                cols.append({'name': col, 'label': col, 'field': col, 'sortable': True})
        table.columns = cols
        table.rows = filtered_df.to_dict('records')
        table.add_slot('body-cell-Team', f'''
        <q-td key="Team" :props="props">
            <div class="row items-center">
                <img :src="`https://raw.githubusercontent.com/dldelpino/football-charts/refs/heads/main/icons/teams/{competition}/${{encodeURIComponent(props.value)}}.png`" class="w-4 mr-2"/>{{{{props.value}}}}
            </div>   
        </q-td>
        ''')
        table.visible = True

    competitions = ["LaLiga", "Premier League", "Serie A", "Bundesliga", "Ligue 1"]
    seasons = []

    for i in range(25):
        if i < 9:
            seasons.append(f"0{i}/0{i+1}")
        elif i == 9:
            seasons.append(f"09/10")
        else:
            seasons.append(f"{i}/{i+1}")
        
    with ui.row():
        competition_select = ui.select(options = competitions, with_input = True).props('outlined bg-color="white" dense color="green-10"').classes("w-[200px]")
        season_select = ui.select(options = seasons, with_input = True).props('outlined bg-color="white" dense color="green-10"').classes("w-[200px]")
        ui.button("Show results", on_click = show_results).props('outline color="green-10"').classes("h-[40px]")

    table = ui.table(columns = [], rows = [])
    table.visible = False