<template>
    <Chart :key="chartKey" :options="chartOptions"></Chart>
</template>

<script setup>

import { inject, onMounted, ref } from 'vue'
import { Chart } from 'highcharts-vue'

const props = defineProps({
    data: { type: Object, required: true},
    league: { type: String },
    name: { type: String }
})

const leagueCountry = inject('leagueCountry')

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

function drawChart() {
    if (!(Object.keys(props.data).length)) return

    const chartData = Object.entries(props.data).sort((a, b) => b[1] - a[1]).map(([name, y]) => ({name, y}))
    const n = chartData[0].y
    chartData.forEach(item => {
        item.name = `<div class="row no-wrap items-center" style="font-size: 11px;">${item.name}<img src="https://raw.githubusercontent.com/dldelpino/football-charts/refs/heads/main/public/icons/teams/${leagueCountry[props.league]}/${item.name}.png" style="width: 16px; margin-left: 6px;"></div>`
            item.color = `hsl(120, ${(1-item.y/(n+1))*100}%, ${(1-item.y/(n+1))*100}%)`
    })

    chartKey.value++

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
            name: props.name,
            data: chartData,
            pointWidth: 20,
        }],
        credits: {
            enabled: false // elimina la marca de agua
        },
    }
}

onMounted(() => {
    drawChart()
})

</script>

<style>

</style>