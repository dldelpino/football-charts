from nicegui import ui

def render():
    with ui.card().props('flat bordered').classes('p-6 bg-white border border-1 border-[#c2c2c2] '):
        ui.label('About').classes('text-bold text-4xl')
        ui.markdown('''
        This project aims to collect and display football data related to the top 5 European leagues since the 2000/01 season. Contents are divided into the following sections:

        - **Season Standings**: Final table of any league and season.
        - **Position History**: Comparison of teams in the same league that finished in a given position.
        - **Position Frequency**: Number of times that teams in the same league finished in a given position.
        - **Team Trajectory**: Results of a given team over every season.
        - **Average Stats**: Average performance of all teams in a given league.
        - **Promoted Teams**: Performance of promoted teams in the season after promotion.

        In competitions where the number of participating teams has changed at least once (e.g. Ligue 1 and Serie A), teams are sometimes sorted by points per match (PPM).
        '''
        )