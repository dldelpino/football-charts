from nicegui import ui
import pandas as pd

def render():
    def show_results():
        competition = competition_select.value
        path = f"data/{competition.lower().replace(" ", "_")}.csv"
        df = pd.read_csv(path)
        
        seasons_played = df["Team"].value_counts().reset_index().sort_values("Team")["count"].to_list() # temporadas que ha jugado cada equipo (orden alfabético)
        if competition in special_competitions:
            df['PPM'] = df['Points']/df['MP']
            cols = df.columns.to_list()
            cols = cols[0:3] + [cols[-1]] + cols[3:-1]
            df = df[cols] # reordenar las columnas
            # df = df.sort_values(by = "PPM", ascending = False)
        df = df.drop(columns = ["Season", "MP"])
        df = df.groupby("Team").mean().round(4)
        df.columns = ["Avg " + col for col in df.columns]
        df = df.reset_index()
        df["SP"] = seasons_played

        cols = df.columns.to_list()
        cols = [cols[-1]] + [cols[1]] + [cols[0]] + cols[2:-1] 
        df = df[cols] # reordenar las columnas
        if competition in special_competitions:
            df = df.sort_values(by = "Avg PPM", ascending = False)
        else:
            df = df.sort_values(by = "Avg Points", ascending = False)

        cols = []
        for col in df.columns:
            if col == "Team":
                cols.append({'name': col, 'label': col, 'field': col, 'sortable': True, 'align': 'left'})
            elif col == "Avg Points" and competition not in special_competitions:
                cols.append({'name': col, 'label': col, 'field': col, 'sortable': True, 'style': 'font-weight: bold'})
            elif col == "Avg PPM":
                cols.append({'name': col, 'label': col, 'field': col, 'sortable': True, 'style': 'font-weight: bold'})
            else:
                cols.append({'name': col, 'label': col, 'field': col, 'sortable': True})
        table.columns = cols
        table.rows = df.to_dict('records')
        table.add_slot('body-cell-Team', f'''
        <q-td key="Team" :props="props">
            <div class="row items-center">
                <img :src="`/icons/teams/{competition}/${{encodeURIComponent(props.value)}}.png`" class="w-4 mr-2"/>{{{{props.value}}}}
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