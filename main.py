from nicegui import app, ui
from pages import about, position_history, team_trajectory, season_standings, average_stats, promoted_teams, position_frequency, promotion_frequency, relegation_frequency

app.add_static_files('/icons', 'icons')

ui.add_head_html('''
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: Inter, sans-serif;
            background-color: whitesmoke;
        }
    </style>
''')

buttons = {}
active_button = None

pages = {
    'About': about.render,
    'Season Standings': season_standings.render,
    'Position History': position_history.render,
    'Position Frequency': position_frequency.render,
    'Team Trajectory': team_trajectory.render,
    'Average Stats': average_stats.render,
    'Promoted Teams': promoted_teams.render,
    'Promotion Frequency': promotion_frequency.render,
    'Relegation Frequency': relegation_frequency.render
}

tables = ['Season Standings', 'Position History', 'Team Trajectory', 'Average Stats', 'Promoted Teams']
pie_charts = ['Position Frequency']
bar_charts = ['Promotion Frequency', 'Relegation Frequency']

tables.sort()
pie_charts.sort()
bar_charts.sort()

def change_page(page):
    content.clear()
    with content:
        pages[page]() # ejecuta la función page.render
    for button_name, button in buttons.items():
        if button_name == page:
            button.props('flat color="green-10" no-caps').style('background-color: #e6e6e6; font-weight: 500; border-radius: 10px')
            active_button = button
        else:
            button.props('flat color="black" no-caps').style('background-color: transparent; font-weight: 500; border-radius: 10px')

with ui.left_drawer(top_corner = True, bottom_corner = True).style('background-color: white; outline-style: solid; outline-color: #c2c2c2; outline-width: 1px'):

    with ui.row().classes('items-center'): # título
        ui.image('icons/ball.png').classes('w-10')
        ui.label('Football Charts').classes('text-xl font-bold')

    ui.label('GENERAL').classes('text-[#616161] text-xs font-[500]')

    button = ui.button(on_click = lambda n = 'About': change_page(n)).props('flat color="green-10" no-caps').style('background-color: #e6e6e6; font-weight: 500; border-radius: 10px') # n = page quiere decir que el valor por defecto de n es page
    with button:
        ui.image('icons/about.png').classes('w-5 mr-3')
        ui.label('About')
    buttons['About'] = button

    ui.label('TABLES').classes('text-[#616161] text-xs font-[500]')

    for page in tables:
        button = ui.button(on_click = lambda n = page: change_page(n)).props('flat color="black" no-caps').style('font-weight: 500; border-radius: 10px')
        with button:
            ui.image('icons/table.png').classes('w-5 mr-3')
            ui.label(page)
        buttons[page] = button

    ui.label('PIE CHARTS').classes('text-[#616161] text-xs font-[500]')

    for page in pie_charts:
        button = ui.button(on_click = lambda n = page: change_page(n)).props('flat color="black" no-caps').style('font-weight: 500; border-radius: 10px')
        with button:
            ui.image('icons/pie.png').classes('w-5 mr-3')
            ui.label(page)
        buttons[page] = button

    ui.label('BAR CHARTS').classes('text-[#616161] text-xs font-[500]')

    for page in bar_charts:
        button = ui.button(on_click = lambda n = page: change_page(n)).props('flat color="black" no-caps').style('font-weight: 500; border-radius: 10px')
        with button:
            ui.image('icons/bar.png').classes('w-5 mr-3')
            ui.label(page)
        buttons[page] = button
    
with ui.column().style('flex-grow: 1; padding: 2em').classes('w-full items-center') as content: # contenedor central donde se carga cada vista
    about.render()  # vista inicial

ui.run(title = 'Football Charts', favicon = 'icons/ball.png', on_air = 'EJsWge0eplJ1AHbh')