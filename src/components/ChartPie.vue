<template>
    <div style="width: 90%">
        <Chart :key="chartKey" :options="chartOptions"></Chart>
    </div> 
</template>

<script setup>

import { inject, onMounted, ref } from 'vue'
import { Chart } from 'highcharts-vue'

const props = defineProps({
    data: { type: Object, required: true},
    league: { type: String },
    position: { type: Number }
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
    const n = Object.keys(props.data).length
    const colors = []
    for (let i = 1; i <= n; i++) {
        colors.push(`hsl(120, ${Math.floor(i/(n+1)*100)}%, ${Math.floor(i/(n+1)*100)}%)`)
    }

    let positionOrdinal
    if (props.position == 1 || props.position == 21) {
        positionOrdinal = 'st'
    } else if (props.position == 2 || props.position == 22) {
        positionOrdinal = 'nd'
    } else if (props.position == 3) {
        positionOrdinal = 'rd'
    } else {
        positionOrdinal = 'th'
    }

    chartKey.value++

    chartOptions.value = {
        title: {
            text: ''
        },
        chart: {
            backgroundColor: '#eeeeee',
            type: 'pie',
            height: 500,
        },
        colors: colors,
        plotOptions: {
            pie: {
                dataLabels: {
                    enabled: true,
                    useHTML: true,
                    style: {
                        fontFamily: 'Inter'
                    },
                    formatter: function() {
                        return `<div class="row no-wrap items-center" style="font-size: 11px"><img src="https://raw.githubusercontent.com/dldelpino/football-charts/refs/heads/main/public/icons/teams/${leagueCountry[props.league]}/${this.point.name}.png" style="width: 16px; margin-right: 6px">${this.point.name} (${this.point.y}) &#8203 &#8203 &#8203 &#8203 &#8203</div>` // &#8203 añade espacio en blanco
                    }
                }
            }
        },
        series: [{
            name: `Times finished ${props.position}${positionOrdinal}`,
            data: chartData
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