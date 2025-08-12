from nicegui import ui
import pandas as pd

def render():
    def filter_by_team(competition, team):
        path = f"data/{competition.lower().replace(" ", "_")}.csv"
        df = pd.read_csv(path)
        filtered_df = df[df["Team"] == team]
        return filtered_df.sort_values(by = "Points", ascending = False)

    def teams_list(competition):
        path = f"data/{competition.lower().replace(" ", "_")}.csv"
        df = pd.read_csv(path)
        return df["Team"].unique().tolist()

    def set_teams(e):
        for i in range(len(competitions)):
            if i == competitions.index(e.value):
                team_selects[i].classes(remove = "hidden")
            else:
                team_selects[i].classes(add = "hidden")
    
    def show_results():
        competition = competition_select.value
        i = competitions.index(competition)
        team = team_selects[i].value
        df = filter_by_team(competition, team)
        if competition in special_competitions:
            df['PPM'] = df['Points']/df['MP']
            df = df.round(4)
            cols = df.columns.to_list()
            cols = cols[0:3] + [cols[-1]] + cols[3:-1]
            df = df[cols] # reordenar las columnas
            df = df.sort_values(by = "PPM", ascending = False)
        cols = []
        for col in df.columns:
            if col == "Team":
                cols.append({'name': col, 'label': col, 'field': col, 'sortable': True, 'align': 'left'})
            elif col == "Points" and competition not in special_competitions:
                cols.append({'name': col, 'label': col, 'field': col, 'sortable': True, 'style': 'font-weight: bold'})
            elif col == "PPM":
                cols.append({'name': col, 'label': col, 'field': col, 'sortable': True, 'style': 'font-weight: bold'})
            else:
                cols.append({'name': col, 'label': col, 'field': col, 'sortable': True})
        table.columns = cols
        table.rows = df.to_dict('records')
        table.add_slot('body-cell-Team', f'''
        <q-td key="Team" :props="props">
            <div class="row items-center">
                <img :src="`https://raw.githubusercontent.com/dldelpino/football-charts/refs/heads/main/icons/teams/{competition}/${{encodeURIComponent(props.value)}}.png`" class="w-4 mr-2"/>{{{{props.value}}}}
            </div>   
        </q-td>
        ''')
        table.visible = True

    competitions = ["LaLiga", "Premier League", "Serie A", "Bundesliga", "Ligue 1"]
    special_competitions = ["Serie A", "Ligue 1"] # competiciones que han cambiado el número de equipos
    team_selects = []

    with ui.row():
        competition_select = ui.select(options = competitions, with_input = True, on_change = set_teams).props('outlined bg-color="white" dense color="green-10"').classes("w-[200px]")
        for competition in competitions:
            team_selects.append(ui.select(new_value_mode = True, options = teams_list(competition), with_input = True).props('outlined bg-color="white" dense color="green-10"').classes("w-[200px] hidden"))
        ui.button("Show results", on_click = show_results).props('outline color="green-10"').classes("h-[40px]")

    table = ui.table(columns = [], rows = [])
    table.visible = False