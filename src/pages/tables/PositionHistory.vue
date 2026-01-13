<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <SelectNumber v-model.number="position" :disable="!league" label="#"/>
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
import SelectLeague from 'src/components/SelectLeague.vue'
import SelectNumber from 'src/components/SelectNumber.vue'
import ShowResults from 'src/components/ShowResults.vue'

const league = ref(null)
const position = ref(null)
const maxPosition = ref(null)

const leaguePositions = inject('leaguePositions')
const specialLeagues = inject('specialLeagues')
const tableLegend = inject('tableLegend')

const rows = ref([])
let columns

const loading = ref(false)
const showMessage = ref(false)

const loadData = async () => {
    if (!league.value || !position.value) return

    loading.value = true
    const timeout = setTimeout(() => {
        showMessage.value = true
    }, 10000)

    if (specialLeagues.includes(league.value)) {
        columns = ref([
            {name: "status", field: "status", label: "", sortable: false, style: "width: 8px; padding: 0", headerStyle: "width: 8px; padding: 0"},
            {name: "season", field: "season", label: "Season", sortable: true},
            {name: "position", field: "position", label: "#", sortable: true},
            {name: "team", field: "team", label: "Team", sortable: true, align: "left", style: "width: 270px"},
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

    const res = await axios.get("https://football-charts-backend.onrender.com/position-history", {
        // local: http://localhost:8000/position-history
        // online: https://football-charts-backend.onrender.com/position-history
        params: {
            league_name: league.value,
            position: position.value
        }
    })

    clearTimeout(timeout)
    loading.value = false
    showMessage.value = false

    rows.value = res.data
}

watch(league, () => {
    position.value = null
})

watch(league, (newLeague) => {
    maxPosition.value = leaguePositions[newLeague]
})

watch(position, (newPosition) => {
    if (newPosition > maxPosition.value) position.value = maxPosition.value
    else if (!(position.value == null) && position.value < 1) position.value = 1
})

const activeTableLegend = computed(() => 
    tableLegend.filter(item => 
        rows.value.some(row => row.status == item.key)
    )
)

</script>

<style>

</style>