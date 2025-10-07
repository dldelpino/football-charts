<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <ShowResults @click="loadData"/>
    </div>
    <div class="buttons-container" style="padding-bottom: 30px">
        <Chart :key="chartKey" :options="chartOptions"></Chart>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { Chart } from 'highcharts-vue'
import ShowResults from '../../components/ShowResults.vue'
import SelectLeague from '../../components/SelectLeague.vue'

const league = ref(null)
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
const chartKey = ref(0)

const leaguesCountries = {
    "LaLiga": "Spain",
    "Premier League": "England",
    "Serie A": "Italy",
    "Bundesliga": "Germany",
    "Ligue 1": "France"
}

const loadData = async () => {
    if (!league.value) return
    const res = await axios.get("https://football-charts-backend.onrender.com/relegation-frequency", {
        params: {
            league_name: league.value
        }
    })
    const relegationCount = res.data

    chartKey.value++

    const chartData = Object.entries(relegationCount).sort((a, b) => b[1] - a[1]).map(([name, y]) => ({name, y}))

    const n = chartData[0].y
    chartData.forEach(item => {
        item.name = `<div class="row no-wrap items-center" style="font-size: 11px;">${item.name}<img src="https://raw.githubusercontent.com/dldelpino/football-charts/refs/heads/main/public/icons/teams/${leaguesCountries[league.value]}/${item.name}.png" style="width: 16px; margin-left: 6px;"></div>`
        item.color = `hsl(120, ${(1-item.y/(n+1))*100}%, ${(1-item.y/(n+1))*100}%)`
    })

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
            name: 'Times relegated',
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
    margin-top: 30px;
    background-color: inherit;
}

.select {
    width: 200px;
}

</style>