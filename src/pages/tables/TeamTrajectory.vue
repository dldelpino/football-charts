<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <SelectTeam :options="teamOptions" v-model="team" :disable="!league"/>
        <ShowResults @click="loadData"/>
    </div>
    <div class="buttons-container" style="padding-bottom: 30px">
        <q-spinner-puff style="margin-top: 50px" v-if="loading" color="green-10" size="50px" :thickness="10"/>
        <q-table class="stats-table" flat bordered v-if="rows.length && !loading" :rows="rows" :columns="columns" virtual-scroll hide-bottom :rows-per-page-options="[0]">
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
import ShowResults from '../../components/ShowResults.vue'
import SelectLeague from '../../components/SelectLeague.vue'
import SelectTeam from '../../components/SelectTeam.vue'
import axios from 'axios'

const league = ref(null)
const team = ref(null)

const rows = ref([])
let columns

const loading = ref(false)

const leagueTeams = {
    "LaLiga": [
        'Barcelona', 'Málaga', 'Deportivo', 'Athletic Bilbao', 'Real Madrid', 'Valencia', 'Real Sociedad', 'Racing Santander', 'Zaragoza', 'Espanyol', 'Las Palmas', 'Alavés', 'Mallorca', 'Valladolid', 'Numancia', 'Oviedo', 'Osasuna', 'Celta', 'Villarreal', 'Rayo Vallecano', 'Betis', 'Sevilla', 'Tenerife', 'Atlético Madrid', 'Recreativo', 'Albacete', 'Murcia', 'Levante', 'Getafe', 'Cádiz', 'Gimnàstic', 'Almería', 'Sporting Gijón', 'Xerez', 'Hércules', 'Granada', 'Elche', 'Eibar', 'Córdoba', 'Leganés', 'Girona', 'Huesca'
    ].sort(),
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

const teamOptions = computed(() => {
    return leagueTeams[league.value]
})

const loadData = async () => {
    loading.value = true
    if (!league.value || !team.value) return
    else if (league.value == "Serie A" || league.value == "Ligue 1") {
        columns = ref([
            {name: "season", field: "season", label: "Season", sortable: true},
            {name: "position", field: "position", label: "#", sortable: true},
            {name: "team", field: "team", label: "Team", sortable: true, align: "left", style: "width: 250px"},
            {name: "ppm", field: "ppm", label: "PPM", sortable: true, style: "width: 70px; font-weight: bold"},
            {name: "points", field: "points", label: "Points", sortable: true, style: "width: 70px"},
            {name: "matches_played", field: "matches_played", label: "MP", sortable: true, style: "width: 70px"},
            {name: "wins", field: "wins", label: "W", sortable: true, style: "width: 70px"},
            {name: "draws", field: "draws", label: "D", sortable: true, style: "width: 70px"},
            {name: "losses", field: "losses", label: "L", sortable: true, style: "width: 70px"},
            {name: "goals_for", field: "goals_for", label: "GF", sortable: true, style: "width: 70px"},
            {name: "goals_against", field: "goals_against", label: "GA", sortable: true, style: "width: 70px"},
            {name: "goal_difference", field: "goal_difference", label: "GD", sortable: true, style: "width: 70px"}
        ])
    }
    else {
        columns = ref([
            {name: "season", field: "season", label: "Season", sortable: true},
            {name: "position", field: "position", label: "#", sortable: true},
            {name: "team", field: "team", label: "Team", sortable: true, align: "left", style: "width: 250px"},
            {name: "points", field: "points", label: "Points", sortable: true, style: "width: 70px; font-weight: bold"},
            {name: "matches_played", field: "matches_played", label: "MP", sortable: true, style: "width: 70px"},
            {name: "wins", field: "wins", label: "W", sortable: true, style: "width: 70px"},
            {name: "draws", field: "draws", label: "D", sortable: true, style: "width: 70px"},
            {name: "losses", field: "losses", label: "L", sortable: true, style: "width: 70px"},
            {name: "goals_for", field: "goals_for", label: "GF", sortable: true, style: "width: 70px"},
            {name: "goals_against", field: "goals_against", label: "GA", sortable: true, style: "width: 70px"},
            {name: "goal_difference", field: "goal_difference", label: "GD", sortable: true, style: "width: 70px"}
        ])
    }
    const res = await axios.get("https://football-charts-backend.onrender.com/team-trajectory", {
        params: {
            team_name: team.value
        }
    })
    loading.value = false
    rows.value = res.data
}

// function loadData() {
//     fetch(`data/${league.value.toLowerCase().replace(/\s+/g, "_")}.csv`)
//         .then(response => response.text())
//         .then(csvText => {
//             Papa.parse(csvText, {
//                 header: true,
//                 complete: results => {
//                     teamTrajectory.value = results.data.map(row => ({
//                         season: row["Season"],
//                         position: Number(row["#"]),
//                         team: row["Team"],
//                         points: Number(row["Points"]),
//                         mp: row["MP"],
//                         w: Number(row["W"]),
//                         d: Number(row["D"]),
//                         l: Number(row["L"]),
//                         gf: Number(row["GF"]),
//                         ga: Number(row["GA"]),
//                         gd: Number(row["GD"]),
//                         top_scorer: row["Top Scorer"],
//                         top_scorer_goals: Number(row["Top Scorer Goals"]),
//                         logo: `icons/teams/${league.value}/${row["Team"]}.png`
//                     }))
//                     rows.value = teamTrajectory.value.filter(row => row.team == team.value).sort((a, b) => b.points - a.points)
//                 }
//             })
//         })
// }

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