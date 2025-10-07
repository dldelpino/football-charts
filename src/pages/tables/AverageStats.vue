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
import axios from 'axios'
import ShowResults from '../../components/ShowResults.vue'
import SelectLeague from '../../components/SelectLeague.vue'

const league = ref(null)

const rows = ref([])
let columns

const loadData = async () => {
    if (!league.value) return
    else if (league.value == "Serie A" || league.value == "Ligue 1") {
        columns = ref([
            {name: "seasons_played", field: "seasons_played", label: "SP", sortable: true},
            {name: "avg_position", field: "avg_position", label: "Avg #", sortable: true},
            {name: "team", field: "team", label: "Team", sortable: true, align: "left", style: "width: 180px"},
            {name: "avg_ppm", field: "avg_ppm", label: "Avg PPM", sortable: true, style: "width: 70px; font-weight: bold"},
            {name: "avg_points", field: "avg_points", label: "Avg Points", sortable: true, style: "width: 70px"},
            {name: "avg_wins", field: "avg_wins", label: "Avg W", sortable: true, style: "width: 70px"},
            {name: "avg_draws", field: "avg_draws", label: "Avg D", sortable: true, style: "width: 70px"},
            {name: "avg_losses", field: "avg_losses", label: "Avg L", sortable: true, style: "width: 70px"},
            {name: "avg_goals_for", field: "avg_goals_for", label: "Avg GF", sortable: true, style: "width: 70px"},
            {name: "avg_goals_against", field: "avg_goals_against", label: "Avg GA", sortable: true, style: "width: 70px"},
            {name: "avg_goal_difference", field: "avg_goal_difference", label: "Avg GD", sortable: true, style: "width: 70px"},
        ])  
    }
    else {
        columns = ref([
            {name: "seasons_played", field: "seasons_played", label: "SP", sortable: true},
            {name: "avg_position", field: "avg_position", label: "Avg #", sortable: true},
            {name: "team", field: "team", label: "Team", sortable: true, align: "left", style: "width: 180px"},
            {name: "avg_points", field: "avg_points", label: "Avg Points", sortable: true, style: "width: 70px; font-weight: bold"},
            {name: "avg_wins", field: "avg_wins", label: "Avg W", sortable: true, style: "width: 70px"},
            {name: "avg_draws", field: "avg_draws", label: "Avg D", sortable: true, style: "width: 70px"},
            {name: "avg_losses", field: "avg_losses", label: "Avg L", sortable: true, style: "width: 70px"},
            {name: "avg_goals_for", field: "avg_goals_for", label: "Avg GF", sortable: true, style: "width: 70px"},
            {name: "avg_goals_against", field: "avg_goals_against", label: "Avg GA", sortable: true, style: "width: 70px"},
            {name: "avg_goal_differene", field: "avg_goal_difference", label: "Avg GD", sortable: true, style: "width: 70px"},
        ])
    }
    const res = await axios.get("https://football-charts-backend.onrender.com/average-stats", {
        params: {
            league_name: league.value
        }
    })
    rows.value = res.data

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