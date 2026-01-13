// variables globales
// para usar un boot file hay que incluir el nombre de este archivo en quasar.config.js

import { boot } from 'quasar/wrappers'

export default boot(({ app }) => {

    const tableLegend = [
        {key: 0, label: "Champions League", color: "#2B3C9C"},
        {key: 1, label: "Champions League qualifiers", color: "#4F62CF"},
        {key: 2, label: "Europa League", color: "#F77F00"},
        {key: 3, label: "Europa League qualifiers", color: "#FF9C33"},
        {key: 4, label: "Conference League", color: "#2DB443"},
        {key: 5, label: "Conference League qualifiers", color: "#2DB443"},
        {key: 6, label: "Intertoto", color: "#909090"},
        {key: 7, label: "Promotion", color: "#2DB443"},
        {key: 8, label: "Promotion play-offs", color: "#5CD670"},
        {key: 9, label: "Relegation play-offs", color: "#D94545"},
        {key: 10, label: "Relegation", color: "#A52222"}, // si cambio el color, cambiarlo también en ChartTable.vue
        {key: 11, label: "Europa League", color: "#F77F00"}, // y descenso
        {key: 12, label: "Europa League qualifiers", color: "#FF9C33"}, // y descenso
    ]

    const leagueCountry = {
        "LaLiga": "Spain",
        "LaLiga2": "Spain",
        "Premier League": "England",
        "Serie A": "Italy",
        "Bundesliga": "Germany",
        "Ligue 1": "France"
    }

    const leagueTeams = { // generado con ayuda de los scripts del backend
        "LaLiga": [
            'Barcelona', 'Málaga', 'Deportivo', 'Athletic Bilbao', 'Real Madrid', 'Valencia', 'Real Sociedad', 'Racing Santander', 'Zaragoza', 'Espanyol', 'Las Palmas', 'Alavés', 'Mallorca', 'Valladolid', 'Numancia', 'Oviedo', 'Osasuna', 'Celta', 'Villarreal', 'Rayo Vallecano', 'Betis', 'Sevilla', 'Tenerife', 'Atlético Madrid', 'Recreativo', 'Albacete', 'Murcia', 'Levante', 'Getafe', 'Cádiz', 'Gimnàstic', 'Almería', 'Sporting Gijón', 'Xerez', 'Hércules', 'Granada', 'Elche', 'Eibar', 'Córdoba', 'Leganés', 'Girona', 'Huesca'
        ].sort((a, b) => a.localeCompare(b, "es")), // para ordenar correctamente las tildes
        "LaLiga2": [
            'Málaga', 'Deportivo', 'Real Sociedad', 'Racing Santander', 'Zaragoza', 'Espanyol', 'Las Palmas', 'Alavés', 'Mallorca', 'Valladolid', 'Numancia', 'Oviedo', 'Osasuna', 'Celta', 'Villarreal', 'Rayo Vallecano', 'Betis', 'Sevilla', 'Tenerife', 'Atlético Madrid', 'Recreativo', 'Albacete', 'Murcia', 'Levante', 'Getafe', 'Cádiz', 'Gimnàstic', 'Almería', 'Sporting Gijón', 'Xerez', 'Hércules', 'Granada', 'Elche', 'Eibar', 'Córdoba', 'Leganés', 'Girona', 'Huesca', 'Lleida', 'Compostela', 'Salamanca', 'Real Jaén', 'Racing Ferrol', 'CF Extremadura', 'Badajoz', 'Universidad Las Palmas', 'Poli Ejido', 'Burgos', 'Terrassa', 'Atlético Malagueño', 'Ciudad de Murcia', 'Algeciras', 'Pontevedra', 'Lorca Deportiva', 'Real Madrid Castilla', 'Castellón', 'Ponferradina', 'Vecindario', 'Granada 74', 'Sevilla Atlético', 'Alicante', 'Cartagena', 'Real Unión', 'Villarreal B', 'Barça Atlètic', 'Alcorcón', 'Alcoyano', 'Guadalajara', 'Sabadell', 'Mirandés', 'Lugo', 'Llagostera', 'Bilbao Athletic', 'Reus', 'UCAM Murcia', 'Cultural Leonesa', 'Extremadura UD', 'Rayo Majadahonda', 'Fuenlabrada', 'Logroñés', 'Ibiza', 'Real Sociedad B', 'Amorebieta', 'Andorra', 'Eldense'
        ].sort((a, b) => a.localeCompare(b, "es")),
        "Premier League": [
            'Charlton', 'Manchester City', 'Chelsea', 'West Ham', 'Coventry', 'Middlesbrough', 'Derby', 'Southampton', 'Leeds', 'Everton', 'Leicester', 'Aston Villa', 'Liverpool', 'Bradford', 'Sunderland', 'Arsenal', 'Tottenham', 'Ipswich', 'Manchester United', 'Newcastle', 'Blackburn', 'Bolton', 'Fulham', 'West Brom', 'Birmingham', 'Wolves', 'Portsmouth', 'Norwich', 'Crystal Palace', 'Wigan', 'Watford', 'Reading', 'Sheffield', 'Stoke', 'Hull', 'Burnley', 'Blackpool', 'QPR', 'Swansea', 'Cardiff', 'Bournemouth', 'Brighton', 'Huddersfield', 'Brentford', 'Nottingham Forest', 'Luton'
        ].sort(),
        "Serie A": [
            'Bari', 'Verona', 'Napoli', 'Juventus', 'Atalanta', 'Lazio', 'Milan', 'Vicenza', 'Parma', 'Fiorentina', 'Perugia', 'Lecce', 'Reggina', 'Inter', 'Roma', 'Bologna', 'Udinese', 'Brescia', 'Chievo', 'Venezia', 'Piacenza', 'Torino', 'Como', 'Empoli', 'Modena', 'Sampdoria', 'Siena', 'Ancona', 'Livorno', 'Cagliari', 'Palermo', 'Messina', 'Ascoli', 'Treviso', 'Catania', 'Genoa', 'Cesena', 'Novara', 'Pescara', 'Sassuolo', 'Frosinone', 'Carpi', 'Crotone', 'SPAL', 'Benevento', 'Spezia', 'Salernitana', 'Monza', 'Cremonese'
        ].sort(),
        "Bundesliga": [
            'Dortmund', 'Hansa Rostock', 'Bayern München', 'Hertha', 'Freiburg', 'Stuttgart', 'Hamburger', '1860 München', 'Kaiserslautern', 'Bochum', 'Leverkusen', 'Wolfsburg', 'Werder Bremen', 'Energie Cottbus', 'Eintracht Frankfurt', 'Unterhaching', 'Schalke', 'Köln', 'Nürnberg', 'Mönchengladbach', 'St. Pauli', 'Arminia', 'Hannover', 'Mainz', 'Duisburg', 'Aachen', 'Karlsruher', 'Hoffenheim', 'Augsburg', 'Fortuna Düsseldorf', 'Greuther Fürth', 'Eintracht Braunschweig', 'Paderborn', 'Darmstadt', 'Ingolstadt', 'RB Leipzig', 'Union Berlin', 'Heidenheim', 'Holstein Kiel'
        ].sort(),
        "Ligue 1": [
            'Marseille', 'Troyes', 'PSG', 'Strasbourg', 'Auxerre', 'Sedan', 'Bordeaux', 'Metz', 'Guingamp', 'Saint-Étienne', 'Lille', 'Monaco', 'Olympique Lyonnais', 'Stade Rennais', 'Nantes', 'Lens', 'Toulouse', 'Bastia', 'Lorient', 'Sochaux', 'Montpellier', 'Nice', 'Le Havre', 'Ajaccio', 'Le Mans', 'Caen', 'Istres', 'Nancy', 'Valenciennes', 'Grenoble', 'Boulogne', 'Arles-Avignon', 'Stade Brestois', 'Evian', 'Dijon', 'Reims', 'Angers', 'Gazélec Ajaccio', 'Amiens', 'Nîmes', 'Clermont'
        ].sort()
    }

    const leaguePositions = {
        "LaLiga": 20,
        "LaLiga2": 22,
        "Premier League": 20,
        "Serie A": 20,
        "Bundesliga": 18,
        "Ligue 1": 20
    }

    const specialLeagues = ["Serie A", "Ligue 1"] // ligas en las que se ha cambiado el número de equipos y requieren de columnas adicionales en algunos casos

    app.provide('leagueCountry', leagueCountry)
    app.provide('leagueTeams', leagueTeams)
    app.provide('leaguePositions', leaguePositions)
    app.provide('specialLeagues', specialLeagues)
    app.provide('tableLegend', tableLegend)
})