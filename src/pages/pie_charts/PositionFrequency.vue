<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <SelectNumber v-model.number="position" :disable="!league" label="Pos."/>
        <ShowResults @click="loadData"/>
    </div>
    <div class="data-container">
        <LoadingSpinner v-if="loading"/>
        <LoadingMessage :class="{visible: showMessage}"/>
        <ChartPie v-if="!loading" :data="data" :league="league" :position="position"/>
    </div>
</template>

<script setup>

import { inject, ref, watch } from 'vue'
import axios from 'axios'

import ChartPie from 'src/components/ChartPie.vue'
import LoadingMessage from 'src/components/LoadingMessage.vue'
import LoadingSpinner from 'src/components/LoadingSpinner.vue'
import SelectLeague from 'src/components/SelectLeague.vue'
import SelectNumber from 'src/components/SelectNumber.vue'
import ShowResults from 'src/components/ShowResults.vue'

const league = ref(null)
const position = ref(null)
const maxPosition = ref(null)

const leaguePositions = inject('leaguePositions')

const data = ref([])

const loading = ref(false)
const showMessage = ref(false)

const loadData = async () => {
    if (!league.value || !position.value) return

    loading.value = true
    const timeout = setTimeout(() => {
        showMessage.value = true
    }, 10000)

    const res = await axios.get("https://football-charts-backend.onrender.com/position-frequency", {
        // local: http://localhost:8000/position-frequency
        // online: https://football-charts-backend.onrender.com/position-frequency
        params: {
            league_name: league.value,
            position: position.value
        }
    })

    clearTimeout(timeout)
    loading.value = false
    showMessage.value = false

    data.value = res.data
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

</script>

<style>

</style>