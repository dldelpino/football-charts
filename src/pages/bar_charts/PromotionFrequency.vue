<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <ShowResults @click="loadData"/>
    </div>
    <div class="data-container">
        <LoadingSpinner v-if="loading"/>
        <LoadingMessage :class="{visible: showMessage}"/>
        <ChartBar v-if="!loading" :data="data" :league="league" :name="'Times promoted'"/>
    </div>
</template>

<script setup>

import { ref } from 'vue'
import axios from 'axios'

import ChartBar from 'src/components/ChartBar.vue'
import LoadingMessage from 'src/components/LoadingMessage.vue'
import LoadingSpinner from 'src/components/LoadingSpinner.vue'
import SelectLeague from 'src/components/SelectLeague.vue'
import ShowResults from 'src/components/ShowResults.vue'

const league = ref(null)

const data = ref([])

const loading = ref(false)
const showMessage = ref(false)

const loadData = async () => {
    if (!league.value) return

    loading.value = true
    const timeout = setTimeout(() => {
        showMessage.value = true
    }, 10000)

    const res = await axios.get("https://football-charts-backend.onrender.com/promotion-frequency", {
        // local: http://localhost:8000/promotion-frequency
        // online: https://football-charts-backend.onrender.com/promotion-frequency
        params: {
            league_name: league.value
        }
    })

    clearTimeout(timeout)
    loading.value = false
    showMessage.value = false

    data.value = res.data
}

</script>

<style>

</style>