<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <SelectPosition v-model.number="position" :disable="!league" :max="maxPosition"/>
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
import { ref, watch } from 'vue'
import Papa from 'papaparse'
import ShowResults from '../../components/ShowResults.vue'
import SelectLeague from '../../components/SelectLeague.vue'
import SelectPosition from '../../components/SelectPosition.vue'

const league = ref(null)
const position = ref(null)

const maxPosition = ref(null)

const rows = ref([])
let columns

const positionHistory = ref([])

function loadData() {
    if (league.value == "Serie A" || league.value == "Ligue 1") {
        columns = ref([
            {name: "season", field: "season", label: "Season", sortable: true},
            {name: "position", field: "position", label: "#", sortable: true},
            {name: "team", field: "team", label: "Team", sortable: true, align: "left", style: "width: 180px"},
            {name: "ppm", field: "ppm", label: "PPM", sortable: true, align: "left", style: "width: 70px; font-weight: bold"},
            {name: "points", field: "points", label: "Points", sortable: true, style: "width: 70px"},
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
    } else {
        columns = ref([
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
    }
    positionHistory.value = []
    fetch(`data/${league.value.toLowerCase().replace(/\s+/g, "_")}.csv`)
        .then(response => response.text())
        .then(csvText => {
            Papa.parse(csvText, {
                header: true,
                complete: results => {
                    if (league.value == "Serie A" || league.value == "Ligue 1") {
                        positionHistory.value = results.data.map(row => ({
                            season: row["Season"],
                            position: Number(row["#"]),
                            team: row["Team"],
                            ppm: Math.round(Number(row["Points"])/Number(row["MP"]) * 1000) / 1000,
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
                    } else {
                        positionHistory.value = results.data.map(row => ({
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
                    }
                    positionHistory.value = positionHistory.value.filter(row => row.position == position.value)
                    if (league.value == "Serie A" || league.value == "Ligue 1") {
                        rows.value = positionHistory.value.sort((a, b) => b.ppm - a.ppm)
                    } else {
                        rows.value = positionHistory.value.sort((a, b) => b.points - a.points)
                    }
                }
            })
        })
}

watch(league, () => {
    position.value = null
})

watch(league, (newLeague) => {
    if (newLeague == "Bundesliga") {
        maxPosition.value = 18
    } else {
        maxPosition.value = 20
    }
})

watch(position, () => {
    if (position.value > maxPosition.value) {
        position.value = maxPosition.value
    } else if (!(position.value == null) && position.value < 1) {
        position.value = 1
    }
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