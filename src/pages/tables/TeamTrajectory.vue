<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <SelectTeam :options="teamOptions" v-model="team" :disable="!league"/>
        <ShowResults @click="loadData"/>
    </div>
    <div class="buttons-container" style="padding-bottom: 30px">
        <q-table class="stats-table" flat bordered v-if="rows.length" :rows="rows" :columns="columns" virtual-scroll hide-bottom :rows-per-page-options="[0]">
        <template v-slot:body-cell-team="props">
            <q-td :props="props" style="align-items: center" class="row">
            <img
                :src="props.row.logo"
                style="width: 16px; margin-right: 8px"
            />
            {{ props.row.team }}
            </q-td>
        </template>
        </q-table>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import Papa from 'papaparse'
import ShowResults from '../../components/ShowResults.vue'
import SelectLeague from '../../components/SelectLeague.vue'
import SelectTeam from '../../components/SelectTeam.vue'

const league = ref(null)
const team = ref(null)

const rows = ref([])
const columns = ref([
    {name: "season", field: "season", label: "Season", sortable: true},
    {name: "position", field: "position", label: "#", sortable: true},
    {name: "team", field: "team", label: "Team", sortable: true, align: "left", style: "width: 180px"},
    {name: "points", field: "points", label: "Points", sortable: true, style: "width: 70px; font-weight: bold"},
    {name: "mp", field: "mp", label: "MP", sortable: true, style: "width: 70px"},
    {name: "w", field: "w", label: "W", sortable: true, style: "width: 70px"},
    {name: "d", field: "d", label: "D", sortable: true, style: "width: 70px"},
    {name: "l", field: "l", label: "L", sortable: true, style: "width: 70px"},
    {name: "gf", field: "gf", label: "GF", sortable: true, style: "width: 70px"},
    {name: "ga", field: "ga", label: "GA", sortable: true, style: "width: 70px"},
    {name: "gd", field: "gd", label: "GD", sortable: true, style: "width: 70px"},
    {name: "top_scorer", field: "top_scorer", label: "Top Scorer", sortable: true, style: "width: 220px"},
    {name: "top_scorer_goals", field: "top_scorer_goals", label: "Top Scorer Goals", sortable: true},
])

const teamTrajectory = ref([])

const leagueTeams = { // listas generadas con el script team_trajectory.py
    "LaLiga": [
        'Real Madrid', 'Deportivo', 'Mallorca', 'Barcelona', 'Valencia', 'Celta Vigo', 'Villarreal', 'Málaga', 'Espanyol', 'Alavés', 'Las Palmas', 'Athletic Club', 'Real Sociedad', 'Rayo Vallecano', 'Osasuna', 'Valladolid', 'Zaragoza', 'Oviedo', 'Racing', 'Numancia', 'Betis', 'Sevilla', 'Tenerife', 'Atlético Madrid', 'Recreativo', 'Albacete', 'Real Murcia', 'Getafe', 'Levante', 'Cádiz', 'Gimnàstic', 'Almería', 'Sporting Gijón', 'Xerez', 'Hércules', 'Granada', 'Elche', 'Eibar', 'Córdoba', 'Leganés', 'Girona', 'Huesca'
    ].sort(),
    "Premier League": [
        'Manchester Utd', 'Arsenal', 'Liverpool', 'Leeds United', 'Ipswich Town', 'Chelsea', 'Sunderland', 'Aston Villa', 'Charlton Ath', 'Southampton', 'Newcastle Utd', 'Tottenham', 'Leicester City', 'Middlesbrough', 'West Ham', 'Everton', 'Derby County', 'Manchester City', 'Coventry City', 'Bradford City', 'Blackburn', 'Fulham', 'Bolton', 'Birmingham City', 'West Brom', 'Portsmouth', 'Wolves', 'Crystal Palace', 'Norwich City', 'Wigan Athletic', 'Reading', 'Sheffield Utd', 'Watford', 'Stoke City', 'Hull City', 'Burnley', 'Blackpool', 'Swansea City', 'QPR', 'Cardiff City', 'Bournemouth', 'Brighton', 'Huddersfield', 'Brentford', "Nott'ham Forest", 'Luton Town'
    ].sort(),
    "Serie A": [
        'Roma', 'Juventus', 'Lazio', 'Parma', 'Inter', 'Milan', 'Atalanta', 'Brescia', 'Fiorentina', 'Bologna', 'Perugia', 'Udinese', 'Lecce', 'Hellas Verona', 'Reggina', 'Vicenza', 'Napoli', 'Bari', 'Chievo', 'Torino', 'Piacenza', 'Venezia', 'Modena', 'Empoli', 'Como', 'Sampdoria', 'Siena', 'Ancona', 'Palermo', 'Messina', 'Livorno', 'Cagliari', 'Ascoli', 'Treviso', 'Catania', 'Genoa', 'Cesena', 'Novara', 'Pescara', 'Sassuolo', 'Carpi', 'Frosinone', 'Crotone', 'SPAL', 'Benevento', 'Spezia', 'Salernitana', 'Monza', 'Cremonese'
    ].sort(),
    "Bundesliga": [
        'Bayern Munich', 'Schalke 04', 'Dortmund', 'Leverkusen', 'Hertha BSC', 'Freiburg', 'Werder Bremen', 'Kaiserslautern', 'Wolfsburg', 'Köln', '1860 Munich', 'Hansa Rostock', 'Hamburger SV', 'Energie Cottbus', 'Stuttgart', 'Unterhaching', 'Eint Frankfurt', 'Bochum', 'Gladbach', 'Nürnberg', 'St. Pauli', 'Hannover 96', 'Arminia', 'Mainz 05', 'MSV Duisburg', 'AA Aachen', 'Karlsruher', 'Hoffenheim', 'Augsburg', 'Düsseldorf', 'Greuther Fürth', 'BTSV', 'Paderborn 07', 'Ingolstadt 04', 'Darmstadt 98', 'RB Leipzig', 'Union Berlin', 'Heidenheim', 'Holstein Kiel'
    ].sort(),
    "Ligue 1": [
        'Nantes', 'Lyon', 'Lille', 'Bordeaux', 'Sedan', 'Rennes', 'Troyes', 'Bastia', 'PSG', 'Guingamp', 'Monaco', 'Metz', 'Auxerre', 'Lens', 'Marseille', 'Toulouse', 'Saint-Étienne', 'Strasbourg', 'Sochaux', 'Montpellier', 'Lorient', 'Nice', 'Ajaccio', 'Le Havre', 'Le Mans', 'Caen', 'Istres', 'Nancy', 'Valenciennes', 'Grenoble', 'Boulogne', 'Brest', 'Arles-Avignon', 'Evian', 'Dijon', 'Reims', 'Angers', 'Gazélec Ajaccio', 'Amiens', 'Nîmes', 'Clermont Foot'
    ].sort()
}

const teamOptions = computed(() => {
    return leagueTeams[league.value]
})

function loadData() {
    fetch(`data/${league.value.toLowerCase().replace(/\s+/g, "_")}.csv`)
        .then(response => response.text())
        .then(csvText => {
            Papa.parse(csvText, {
                header: true,
                complete: results => {
                    teamTrajectory.value = results.data.map(row => ({
                        season: row["Season"],
                        position: Number(row["#"]),
                        team: row["Team"],
                        points: Number(row["Points"]),
                        mp: row["MP"],
                        w: Number(row["W"]),
                        d: Number(row["D"]),
                        l: Number(row["L"]),
                        gf: Number(row["GF"]),
                        ga: Number(row["GA"]),
                        gd: Number(row["GD"]),
                        top_scorer: row["Top Scorer"],
                        top_scorer_goals: Number(row["Top Scorer Goals"]),
                        logo: `icons/teams/${league.value}/${row["Team"]}.png`
                    }))
                    rows.value = teamTrajectory.value.filter(row => row.team == team.value).sort((a, b) => b.points - a.points)
                }
            })
        })
}

watch(league, () => { // borra la selección del segundo botón si cambia la del primero
    team.value = null
}) 
</script>

<style>

.buttons-container {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin-top: 30px;
}

.select {
    width: 200px;
}

.stats-table, .stats-table th, .stats-table td {
    border-color: #c2c2c2;
}

.stats-table {
    border-radius: 10px;
}

</style>