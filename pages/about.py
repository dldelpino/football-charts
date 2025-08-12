from nicegui import ui

def render():
    with ui.card().props('flat bordered').classes('p-6 bg-white border border-1 border-[#c2c2c2] '):
        ui.markdown('''
        <h2 style="font-weight: bold; margin: 0">About</h2>
        ---

        This project aims to collect and display football data related to the top 5 European leagues since the 2000/01 season.

        **Tables**

        - *Average Stats*: Average performance of all teams in a given league.
        - *Position History*: Comparison of teams in the same league that finished in a given position.
        - *Promoted Teams*: Performance of promoted teams in the season after promotion.
        - *Season Standings*: Final table of any league and season.
        - *Team Trajectory*: Results of a given team over every season.        

        In competitions where the number of participating teams has changed at least once (e.g. Ligue 1 and Serie A), teams are sometimes sorted by points per match (PPM).

        **Pie Charts**

        - *Position Frequency*: Number of times that teams in the same league finished in a given position.

        **Bar Charts**

        - *Promotion Frequency*: Number of times that teams have been promoted to a given league.
        - *Relegation Frequency*: Number of times that teams have been relegated from a given league.
        
        ''')