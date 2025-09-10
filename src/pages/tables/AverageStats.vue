<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
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

const league = ref(null)

const rows = ref([])
let columns

const stats = ref([])
const averageStats = ref([])

function loadData() {
    if (league.value == "Serie A" || league.value == "Ligue 1") {
        columns = ref([
            {name: "sp", field: "sp", label: "SP", sortable: true},
            {name: "avg_position", field: "avg_position", label: "Avg #", sortable: true},
            {name: "team", field: "team", label: "Team", sortable: true, align: "left", style: "width: 180px"},
            {name: "avg_ppm", field: "avg_ppm", label: "Avg PPM", sortable: true, style: "width: 70px; font-weight: bold"},
            {name: "avg_points", field: "avg_points", label: "Avg Points", sortable: true, style: "width: 70px"},
            {name: "avg_w", field: "avg_w", label: "Avg W", sortable: true, style: "width: 70px"},
            {name: "avg_d", field: "avg_d", label: "Avg D", sortable: true, style: "width: 70px"},
            {name: "avg_l", field: "avg_l", label: "Avg L", sortable: true, style: "width: 70px"},
            {name: "avg_gf", field: "avg_gf", label: "Avg GF", sortable: true, style: "width: 70px"},
            {name: "avg_ga", field: "avg_ga", label: "Avg GA", sortable: true, style: "width: 70px"},
            {name: "avg_gd", field: "avg_gd", label: "Avg GD", sortable: true, style: "width: 70px"},
            {name: "avg_top_scorer_goals", field: "avg_top_scorer_goals", label: "Avg Top Scorer Goals", sortable: true},
        ])
    } else {
        columns = ref([
            {name: "sp", field: "sp", label: "SP", sortable: true},
            {name: "avg_position", field: "avg_position", label: "Avg #", sortable: true},
            {name: "team", field: "team", label: "Team", sortable: true, align: "left", style: "width: 180px"},
            {name: "avg_points", field: "avg_points", label: "Avg Points", sortable: true, style: "width: 70px; font-weight: bold"},
            {name: "avg_w", field: "avg_w", label: "Avg W", sortable: true, style: "width: 70px"},
            {name: "avg_d", field: "avg_d", label: "Avg D", sortable: true, style: "width: 70px"},
            {name: "avg_l", field: "avg_l", label: "Avg L", sortable: true, style: "width: 70px"},
            {name: "avg_gf", field: "avg_gf", label: "Avg GF", sortable: true, style: "width: 70px"},
            {name: "avg_ga", field: "avg_ga", label: "Avg GA", sortable: true, style: "width: 70px"},
            {name: "avg_gd", field: "avg_gd", label: "Avg GD", sortable: true, style: "width: 70px"},
            {name: "avg_top_scorer_goals", field: "avg_top_scorer_goals", label: "Avg Top Scorer Goals", sortable: true},
        ])
    }
    averageStats.value = []
    fetch(`data/${league.value.toLowerCase().replace(/\s+/g, "_")}.csv`)
        .then(response => response.text())
        .then(csvText => {
            Papa.parse(csvText, {
                header: true,
                complete: results => {
                    stats.value = results.data.map(row => ({
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
                    stats.value.forEach(obj => {
                        if (!averageStats.value.some(item => item.team == obj.team)) { // si el equipo no está en el diccionario...
                            const teamSeasons = stats.value.filter(item => item.team == obj.team)
                            const seasonsPlayed = teamSeasons.length
                            const positionSum = teamSeasons.map(item => item.position).reduce((acc, item) => acc + item, 0) // (acumulador, elemento del array) => operaciones a realizar, valor inicial del acumulador
                            const pointsSum = teamSeasons.map(item => item.points).reduce((acc, item) => acc + item, 0)
                            const wSum = teamSeasons.map(item => item.w).reduce((acc, item) => acc + item, 0)
                            const dSum = teamSeasons.map(item => item.d).reduce((acc, item) => acc + item, 0)
                            const lSum = teamSeasons.map(item => item.l).reduce((acc, item) => acc + item, 0)
                            const gfSum = teamSeasons.map(item => item.gf).reduce((acc, item) => acc + item, 0)
                            const gaSum = teamSeasons.map(item => item.ga).reduce((acc, item) => acc + item, 0)
                            const gdSum = teamSeasons.map(item => item.gd).reduce((acc, item) => acc + item, 0)
                            const topScorerGoalsSum = teamSeasons.map(item => item.top_scorer_goals).reduce((acc, item) => acc + item, 0)
                            if (league.value == "Serie A" || league.value == "Ligue 1") {
                                const ppmSum = teamSeasons.map(item => item.points / item.mp).reduce((acc, item) => acc + item, 0)
                                averageStats.value.push({
                                    sp: seasonsPlayed,
                                    avg_position: Math.round(positionSum / seasonsPlayed * 1000) / 1000,
                                    team: obj.team,
                                    avg_ppm: Math.round(ppmSum / seasonsPlayed * 1000) / 1000,
                                    avg_points: Math.round(pointsSum / seasonsPlayed * 1000) / 1000,
                                    avg_w: Math.round(wSum / seasonsPlayed * 1000) / 1000,
                                    avg_d: Math.round(dSum / seasonsPlayed * 1000) / 1000,
                                    avg_l: Math.round(lSum / seasonsPlayed * 1000) / 1000,
                                    avg_gf: Math.round(gfSum / seasonsPlayed * 1000) / 1000,
                                    avg_ga: Math.round(gaSum / seasonsPlayed * 1000) / 1000,
                                    avg_gd: Math.round(gdSum / seasonsPlayed * 1000) / 1000,
                                    avg_top_scorer_goals: Math.round(topScorerGoalsSum / seasonsPlayed * 1000) / 1000,
                                    logo: `icons/teams/${league.value}/${obj.team}.png`,
                                })
                            } else {
                                averageStats.value.push({
                                    sp: seasonsPlayed,
                                    avg_position: Math.round(positionSum / seasonsPlayed * 1000) / 1000,
                                    team: obj.team,
                                    avg_points: Math.round(pointsSum / seasonsPlayed * 1000) / 1000,
                                    avg_w: Math.round(wSum / seasonsPlayed * 1000) / 1000,
                                    avg_d: Math.round(dSum / seasonsPlayed * 1000) / 1000,
                                    avg_l: Math.round(lSum / seasonsPlayed * 1000) / 1000,
                                    avg_gf: Math.round(gfSum / seasonsPlayed * 1000) / 1000,
                                    avg_ga: Math.round(gaSum / seasonsPlayed * 1000) / 1000,
                                    avg_gd: Math.round(gdSum / seasonsPlayed * 1000) / 1000,
                                    avg_top_scorer_goals: Math.round(topScorerGoalsSum / seasonsPlayed * 1000) / 1000,
                                    logo: `icons/teams/${league.value}/${obj.team}.png`,
                                })
                            }
                        }
                    })
                    if (league.value == "Serie A" || league.value == "Ligue 1") {
                        rows.value = averageStats.value.sort((a, b) => b.avg_ppm - a.avg_ppm)
                    } else {
                        rows.value = averageStats.value.sort((a, b) => b.avg_points - a.avg_points)
                    }
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