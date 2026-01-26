<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <SelectTeam v-model="team" v-model:league="league"/>
        <ShowResults @click="loadData"/>
    </div>
    <div class="data-container">
        <LoadingSpinner v-if="loading"/>
        <LoadingMessage :class="{visible: showMessage}"/>
        <q-table :rows="rows" :columns="columns" v-if="!loading" class="streaks-table" separator="cell" flat bordered hide-header hide-bottom :rows-per-page-options="[-1]">
            <template v-slot:body="props">
                <q-tr :props="props"> <!-- filas principales -->
                    <q-td style="width: 500px">
                        <q-btn size="10px" round dense flat @click="props.row.expand = !props.row.expand" :icon="props.row.expand ? 'remove' : 'add'" />
                        <span style="font-weight: bold; margin-left: 10px;">{{ props.row.streak }}</span>
                    </q-td>
                    <q-td style="width: 60px; text-align: center;">
                        <!-- <q-spinner-puff v-if="props.row.loading && !props.row.result" color="secondary" size="25px" :thickness="10"/> -->
                        {{ props.row.result ?? '' }}
                    </q-td>
                    <!-- <q-td style="padding: 0">
                        <q-btn 
                        flat
                        square
                        class="full-width full-height" 
                        color="secondary" 
                        style="font-weight: bold" 
                        label="Show results" 
                        @click="loadData(props.row)" 
                        :disable="!team"/>
                    </q-td> -->
                </q-tr>
                <template v-if="props.row.expand">
                <q-tr v-for="(match, index) in props.row.matches" :key="index"> <!-- filas que se expanden -->
                    <q-td colspan="100%">
                        <div class="expanded-row">
                            <div style="width: 45%; display: flex; justify-content: flex-end;">
                                {{ match[1] }}
                                <img :src="match[2]" style="width: 16px; margin-left: 6px; margin-right: 3px;"/>
                            </div>
                            <div>{{ match[0].home_goals }}</div>
                            <div>-</div>
                            <div>{{ match[0].away_goals }}</div>
                            <div style="width: 45%; display: flex; justify-content: space-between;">
                                <div style="display: flex; justify-content: flex-start;">
                                    <img :src="match[4]" style="width: 16px; margin-left: 3px; margin-right: 6px"/>
                                    {{ match[3] }}
                                </div>
                                <div class="text-grey" style="font-size: 11px; display: flex; align-items: center;">{{ match[0].date }}</div>
                            </div>
                        </div>
                    </q-td>
                </q-tr>
                </template>
            </template>
        </q-table>
    </div>
</template>

<script setup>

import { ref, watch } from 'vue'
import axios from 'axios'

import LoadingMessage from 'src/components/LoadingMessage.vue'
import LoadingSpinner from 'src/components/LoadingSpinner.vue'
import SelectLeague from 'src/components/SelectLeague.vue'
import SelectTeam from 'src/components/SelectTeam.vue'
import ShowResults from 'src/components/ShowResults.vue'

const league = ref(null)
const team = ref(null)

const rows = ref([
    {streak: "Most consecutive wins"},
    {streak: "Most consecutive draws"},
    {streak: "Most consecutive losses"},
    {streak: "Most consecutive matches scoring"},
    {streak: "Most consecutive matches conceding"},
    {streak: "Most consecutive matches without winning"},
    {streak: "Most consecutive matches without drawing"},
    {streak: "Most consecutive matches without losing"},
    {streak: "Most consecutive matches without scoring"},
    {streak: "Most consecutive matches without conceding"}
])
const columns = ref([
    {name: "streak", field: "streak"},
    {name: "result", field: "result"},
    {name: "button", field: "button"}
])

const loading = ref(false)
const showMessage = ref(false)

const loadData = async () => {
    if (!league.value || !team.value) return

    // row.loading = true
    loading.value = true
    const timeout = setTimeout(() => {
        showMessage.value = true
    }, 10000)

    const res = await axios.get("https://football-charts-backend.onrender.com/team-streaks", {
        // local: http://localhost:8000/team-streaks
        // online: https://football-charts-backend.onrender.com/team-streaks
        params: {
            league_name: league.value,
            team_name: team.value,
            // streak: row.streak
        }
    })

    // row.loading = false
    // row.result = res.data.record
    // row.matches = res.data.matches

    clearTimeout(timeout)
    loading.value = false
    showMessage.value = false

    for (let i = 0; i < rows.value.length; i++) {
        rows.value[i].result = res.data[i].record
        rows.value[i].matches = res.data[i].matches
    }

    console.log(res.data)
}

watch(league, () => {
    team.value = null
}) 

</script>

<style>

.streaks-table, .streaks-table th, .streaks-table td {
    border-color: #c2c2c2;
}

.streaks-table {
    border-radius: 10px;
    max-width: 90%;
    font-feature-settings: "tnum";
    margin-top: 40px;
}

.expanded-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.expanded-row div {
    text-align: center;
}
</style>