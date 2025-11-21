<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <ShowResults @click="loadData"/>
    </div>
    <div class="data-container">
        <LoadingSpinner v-if="loading"/>
        <LoadingMessage :class="{visible: showMessage}"/>
        <Chart v-if="!loading" :key="chartKey" :options="chartOptions"></Chart>
    </div>
</template>

<script setup>

import { ref } from 'vue'
import { Chart } from 'highcharts-vue'
import axios from 'axios'

import LoadingMessage from 'src/components/LoadingMessage.vue'
import LoadingSpinner from 'src/components/LoadingSpinner.vue'
import SelectLeague from '../../components/SelectLeague.vue'
import ShowResults from '../../components/ShowResults.vue'

const league = ref(null)

const chartKey = ref(0)
const chartOptions = ref({
    title: {
        text: ''
    },
    chart: {
        backgroundColor: '#eeeeee'
    },
    credits: {
        enabled: false,
    }
})

const loading = ref(false)
const showMessage = ref(false)

const leaguesCountries = {
    "LaLiga": "Spain",
    "LaLiga2": "Spain",
    "Premier League": "England",
    "Serie A": "Italy",
    "Bundesliga": "Germany",
    "Ligue 1": "France"
}

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

    const promotionCount = res.data

    chartKey.value++

    const chartData = Object.entries(promotionCount).sort((a, b) => b[1] - a[1]).map(([name, y]) => ({name, y}))
    const n = chartData[0].y
    chartData.forEach(item => {
        item.name = `<div class="row no-wrap items-center" style="font-size: 11px;">${item.name}<img src="https://raw.githubusercontent.com/dldelpino/football-charts/refs/heads/main/public/icons/teams/${leaguesCountries[league.value]}/${item.name}.png" style="width: 16px; margin-left: 6px;"></div>`
        item.color = `hsl(120, ${(1-item.y/(n+1))*100}%, ${(1-item.y/(n+1))*100}%)`
    })

    clearTimeout(timeout)
    loading.value = false
    showMessage.value = false

    chartOptions.value = {
        title: {
            text: ''
        },
        chart: {
            backgroundColor: '#eeeeee',
            type: 'bar',
            height: 30*chartData.length,
            width: 800,
            marginRight: 20
        },
        tooltip: { // lo que sale al pasar el ratón por encima de una barra
            outside: true
        },
        legend: {
            enabled: false
        },
        xAxis: {
            type: 'category',
            labels: {
                useHTML: true
            }
        },
        yAxis: {
            max: n,
            title: '',
            labels: {
                enabled: false
            }
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true,
                    overflow: 'allow',
                    crop: false,
                    style: {
                        fontFamily: 'Inter'
                    }
                }
            }
        },
        series: [{
            name: 'Times promoted',
            data: chartData,
            pointWidth: 20,
        }],
        credits: {
            enabled: false // elimina la marca de agua
        },
    }
}

</script>

<style>

.buttons-container {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin-top: 40px;
    flex-wrap: wrap;
}

.data-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
}

</style>