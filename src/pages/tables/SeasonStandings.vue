<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <SelectSeason v-model="season" />
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
import { ref } from 'vue'
import Papa from 'papaparse'
import ShowResults from '../../components/ShowResults.vue'
import SelectLeague from '../../components/SelectLeague.vue'
import SelectSeason from '../../components/SelectSeason.vue'

const league = ref(null)
const season = ref(null)
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
const seasonStandings = ref([])

function loadData() {
    fetch(`data/${league.value.toLowerCase().replace(/\s+/g, "_")}.csv`)
        .then(response => response.text())
        .then(csvText => {
            Papa.parse(csvText, {
                header: true,
                complete: results => {
                    seasonStandings.value = results.data.map(row => ({
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
                    rows.value = seasonStandings.value.filter(row => row.season == season.value)
                }
            })
        })
}
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