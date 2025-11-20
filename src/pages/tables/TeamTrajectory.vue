<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <SelectTeam :options="teamOptions" v-model="team" :disable="!league"/>
        <ShowResults @click="loadData"/>
    </div>
    <div class="data-container">
        <LoadingSpinner v-if="loading"/>
        <LoadingMessage :class="{visible: showMessage}"/>
        <q-table class="stats-table" flat bordered v-if="rows.length && !loading" :rows="rows" :columns="columns" virtual-scroll hide-bottom :rows-per-page-options="[0]">
            <template v-slot:body-cell-team="props">
                <q-td :props="props" style="align-items: center" class="row">
                    <img :src="props.row.logo" style="width: 16px; margin-right: 8px"/>
                    {{ props.row.team }}
                </q-td>
            </template>
        </q-table>
    </div>
</template>

<script setup>

import { ref, computed, watch } from 'vue'
import axios from 'axios'

import LoadingMessage from 'src/components/LoadingMessage.vue'
import LoadingSpinner from 'src/components/LoadingSpinner.vue'
import SelectLeague from '../../components/SelectLeague.vue'
import SelectTeam from '../../components/SelectTeam.vue'
import ShowResults from '../../components/ShowResults.vue'

const league = ref(null)
const team = ref(null)

const rows = ref([])
let columns

const loading = ref(false)
const showMessage = ref(false)

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
    if (!league.value || !team.value) return

    loading.value = true
    const timeout = setTimeout(() => {
        showMessage.value = true
    }, 10000)

    if (league.value == "Serie A" || league.value == "Ligue 1") {
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

    clearTimeout(timeout)
    loading.value = false
    showMessage.value = false

    rows.value = res.data
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
    margin-top: 40px;
    flex-wrap: wrap;
}

.data-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 40px;
}

.stats-table, .stats-table th, .stats-table td {
    border-color: #c2c2c2;
}

.stats-table {
    border-radius: 10px;
    max-width: 90%;
    font-feature-settings: "tnum";
}

</style>