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

const promotedTeams = ref([])

function loadPromotedTeams(data) {
    const newData = []
    const seasons = []
    for (let i = 0; i < 25; i++) {
        const year1 = String(i).padStart(2, "0")
        const year2 = String(i+1).padStart(2, "0")
        seasons.push(`${year1}/${year2}`)
    }
    for (let i = 0; i < 25; i++) {
        let season1Promoted
        let season1
        if (i == 0) {
            season1 = seasons[0]
            if (league.value == "LaLiga") {
                season1Promoted = ["Villarreal", "Las Palmas", "Osasuna"]
            } else if (league.value == "Premier League") {
                season1Promoted = ["Ipswich Town", "Charlton Ath", "Manchester City"]
            } else if (league.value == "Serie A") {
                season1Promoted = ["Atalanta", "Vicenza", "Napoli"]
            } else if (league.value == "Bundesliga") {
                season1Promoted = ["Köln", "Energie Cottbus", "Bochum"]
            } else if (league.value == "Ligue 1") {
                season1Promoted = ["Lille", "Guingamp", "Toulouse"]
            }
        } else {
            const season0 = seasons[i-1]
            season1 = seasons[i]
            const teams0 = []
            const teams1 = []
            data.forEach(row => {
                if (row["Season"] == season0) {
                    teams0.push(row["Team"])
                } else if (row["Season"] == season1) {
                    teams1.push(row["Team"])
                }
            })
            season1Promoted = teams1.filter(team => !teams0.includes(team))
        }
        data.forEach(row => {
            if (row["Season"] == season1 && season1Promoted.includes(row["Team"])) {
                newData.push(row)
            }
        })
    }
    return newData
}

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
    promotedTeams.value = []
    fetch(`data/${league.value.toLowerCase().replace(/\s+/g, "_")}.csv`)
        .then(response => response.text())
        .then(csvText => {
            Papa.parse(csvText, {
                header: true,
                complete: results => {
                    if (league.value == "Serie A" || league.value == "Ligue 1") {
                        promotedTeams.value = loadPromotedTeams(results.data).map(row => ({
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
                        promotedTeams.value = loadPromotedTeams(results.data).map(row => ({
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
                    rows.value = promotedTeams.value
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