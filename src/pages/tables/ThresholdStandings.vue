<template>
    <NoDataAvailable v-model="error"/>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <SelectNumber v-model.number="matchesPlayed" :disable="!league" label="MP"/>
        <SelectNumber v-model.number="points" :disable="!matchesPlayed" style="width: 122px;" label="Points"/>
        <ShowResults @click="loadData"/>
    </div>
    <div class="data-container">
        <LoadingSpinner v-if="loading"/>
        <LoadingMessage :class="{visible: showMessage}"/>
        <ChartTable :rows="rows" :columns="columns" :legend="activeTableLegend" v-if="rows.length && !loading"/>
    </div>
</template>

<script setup>

import { computed, inject, ref, watch } from 'vue'
import axios from 'axios'

import ChartTable from 'src/components/ChartTable.vue'
import LoadingMessage from 'src/components/LoadingMessage.vue'
import LoadingSpinner from 'src/components/LoadingSpinner.vue'
import NoDataAvailable from 'src/components/NoDataAvailable.vue'
import SelectLeague from 'src/components/SelectLeague.vue'
import SelectNumber from 'src/components/SelectNumber.vue'
import ShowResults from 'src/components/ShowResults.vue'

const league = ref(null)
const matchesPlayed = ref(null)
const points = ref(null)

const maxMatchesPlayed = ref(null)
const maxPoints = ref(null)

const leaguePositions = inject('leaguePositions')
const specialLeagues = inject('specialLeagues')
const tableLegend = inject('tableLegend')

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

    if (specialLeagues.includes(league.value)) {
        columns = ref([
            {name: "status", field: "status", label: "", sortable: false, style: "width: 8px; padding: 0", headerStyle: "width: 8px; padding: 0"},
            {name: "season", field: "season", label: "Season", sortable: true},
            {name: "position", field: "position", label: "#", sortable: true},
            {name: "team", field: "team", label: "Team", sortable: true, align: "left", style: "width: 270px"},
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
            {name: "status", field: "status", label: "", sortable: false, style: "width: 8px; padding: 0", headerStyle: "width: 8px; padding: 0"},
            {name: "season", field: "season", label: "Season", sortable: true},
            {name: "position", field: "position", label: "#", sortable: true},
            {name: "team", field: "team", label: "Team", sortable: true, align: "left", style: "width: 270px"},
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
    maxMatchesPlayed.value = 2*(leaguePositions[newLeague] - 1)
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

const activeTableLegend = computed(() => 
    tableLegend.filter(item => 
        rows.value.some(row => row.status == item.key)
    )
)

</script>

<style>

</style>