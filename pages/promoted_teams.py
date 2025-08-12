from nicegui import ui
import pandas as pd

def render():
    def show_results():
        competition = competition_select.value
        path = f"data/{competition.lower().replace(" ", "_")}.csv"
        df = pd.read_csv(path)

        seasons = df["Season"].unique().tolist()
        promoted_teams = []
        for i in range(len(seasons)):
            if i == 0:
                season1 = seasons[0]
                if competition == "LaLiga":
                    teams = ["Villarreal", "Las Palmas", "Osasuna"] # equipos recién ascendidos en la 00/01
                elif competition == "Premier League":
                    teams = ["Ipswich Town", "Charlton Ath", "Manchester City"]
                elif competition == "Serie A":
                    teams = ["Atalanta", "Vicenza", "Napoli"]
                elif competition == "Bundesliga":
                    teams = ["Köln", "Energie Cottbus", "Bochum"]
                elif competition == "Ligue 1":
                    teams = ["Lille", "Guingamp", "Toulouse"]
            else:
                season0 = seasons[i-1]
                season1 = seasons[i]
                teams0 = df[df["Season"] == season0]["Team"].to_list()
                teams1 = df[df["Season"] == season1]["Team"].to_list()
                teams = [item for item in teams1 if item not in teams0] # equipos recién ascendidos
            for team in teams:
                promoted_teams.append((season1, team))
        df = df[df.apply(lambda row: (row["Season"], row["Team"]) in promoted_teams, axis = 1)]
        # df = df.sort_values(by = "Points", ascending = False)
        if competition in special_competitions:
            df['PPM'] = df['Points']/df['MP']
            df = df.round(4)
            cols = df.columns.to_list()
            cols = cols[0:3] + [cols[-1]] + cols[3:-1]
            df = df[cols] # reordenar las columnas
            # df = df.sort_values(by = "PPM", ascending = False)
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

    with ui.row():
        competition_select = ui.select(options = competitions, with_input = True).props('outlined bg-color="white" dense color="green-10"').classes("w-[200px]")
        ui.button("Show results", on_click = show_results).props('outline color="green-10"').classes("h-[40px]")
    
    table = ui.table(columns = [], rows = [])
    table.visible = False