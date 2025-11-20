<template>
    <NoDataAvailable v-model="error"/>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>

        <q-input v-model.number="matchesPlayed" :disable="!league" outlined rounded bg-color="white" dense color="secondary" style="width: 110px;" label="MP">
            <template v-slot:append>
                <q-btn round dense flat icon="remove" size="10px" @mousedown="decreaseMatchesPlayed" @mouseup="clear" @mouseleave="clear"/>
                <q-btn round dense flat icon="add" size="10px" @mousedown="increaseMatchesPlayed" @mouseup="clear" @mouseleave="clear"/>
            </template>
        </q-input>

        <q-input v-model.number="points" :disable="!matchesPlayed" outlined rounded bg-color="white" dense color="secondary" style="width: 110px;" label="Pts.">
            <template v-slot:append>
                <q-btn round dense flat icon="remove" size="10px" @mousedown="decreasePoints" @mouseup="clear" @mouseleave="clear"/>
                <q-btn round dense flat icon="add" size="10px" @mousedown="increasePoints" @mouseup="clear" @mouseleave="clear"/>
            </template>
        </q-input>

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

import { ref, watch } from 'vue'
import axios from 'axios'

import LoadingMessage from 'src/components/LoadingMessage.vue'
import LoadingSpinner from 'src/components/LoadingSpinner.vue'
import NoDataAvailable from 'src/components/NoDataAvailable.vue'
import SelectLeague from 'src/components/SelectLeague.vue'
import ShowResults from 'src/components/ShowResults.vue'

const league = ref(null)
const matchesPlayed = ref(null)
const points = ref(null)

const maxMatchesPlayed = ref(null)
const maxPoints = ref(null)

let interval = null
let timeout = null

const decreaseMatchesPlayed = () => {
    matchesPlayed.value--
    timeout = setTimeout(() => {
        interval = setInterval(() => matchesPlayed.value--, 50)
    }, 250)
}
const increaseMatchesPlayed = () => {
    matchesPlayed.value++
    timeout = setTimeout(() => {
        interval = setInterval(() => matchesPlayed.value++, 50)
    }, 250)
}
const decreasePoints = () => {
    points.value--
    timeout = setTimeout(() => {
        interval = setInterval(() => points.value--, 50)
    }, 250)
}
const increasePoints = () => {
    points.value++
    timeout = setTimeout(() => {
        interval = setInterval(() => points.value++, 50)
    }, 250)
}
const clear = () => {
    clearInterval(interval)
    clearTimeout(timeout)
}

const rows = ref([])
let columns

const loading = ref(false)
const showMessage = ref(false)
const error = ref(false)

const loadData = async () => {
    if (!league.value) return

    loading.value = true
    error.value = false
    const timeout = setTimeout(() => {
        showMessage.value = true
    }, 15000)

    if (league.value == "Serie A" || league.value == "Ligue 1") {
        columns = ref([
            {name: "season", field: "season", label: "Season", sortable: true},
            {name: "position", field: "position", label: "#", sortable: true},
            {name: "team", field: "team", label: "Team", sortable: true, align: "left", style: "width: 250px"},
            {name: "ppm_mw", field: "ppm_mw", label: `PPM after ${matchesPlayed.value} MP`, sortable: true, style: "width: 70px"},
            {name: "points_mw", field: "points_mw", label: `Points after ${matchesPlayed.value} MP`, sortable: true, style: "width: 70px"},
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
            {name: "points_mw", field: "points_mw", label: `Points after ${matchesPlayed.value} MP`, sortable: true, style: "width: 70px"},
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

    const res = await axios.get("https://football-charts-backend.onrender.com/threshold-standings", { 
        // local: http://localhost:8000/threshold-standings
        // online: https://football-charts-backend.onrender.com/threshold-standings
        params: {
            league_name: league.value,
            matches_played: matchesPlayed.value,
            threshold: points.value
        }
    })

    clearTimeout(timeout)
    loading.value = false
    showMessage.value = false

    rows.value = res.data

    console.log(!rows.value.length)
    if (!rows.value.length) {
        error.value = true
    }
}

watch(league, () => {
    matchesPlayed.value = null
    points.value = null
})

watch(matchesPlayed, () => {
    points.value = null
})

watch(league, (newLeague) => {
    if (newLeague == "Bundesliga") {
        maxMatchesPlayed.value = 34
    } else {
        maxMatchesPlayed.value = 38
    }
})

watch(matchesPlayed, (newMatchesPlayed) => {
    if (!(newMatchesPlayed == null)) maxPoints.value = 3*newMatchesPlayed
    if (newMatchesPlayed > maxMatchesPlayed.value) matchesPlayed.value = maxMatchesPlayed.value
    else if (!(newMatchesPlayed == null) && newMatchesPlayed < 1) matchesPlayed.value = 1
})

watch(points, (newPoints) => {
    if (newPoints > maxPoints.value) points.value = maxPoints.value
    else if (!(newPoints == null) && newPoints < 0) points.value = 0
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