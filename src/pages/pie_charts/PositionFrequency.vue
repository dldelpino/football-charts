<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <SelectPosition v-model.number="position" :disable="!league" :max="maxPosition"/>
        <ShowResults @click="loadData"/>
    </div>
    <div class="buttons-container" style="padding-bottom: 30px">
        <q-spinner-puff style="margin-top: 50px" v-if="loading" color="secondary" size="50px" :thickness="10"/>
        <div class="chart-container">
            <Chart v-if="!loading" :key="chartKey" :options="chartOptions"></Chart>
        </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Chart } from 'highcharts-vue'
import ShowResults from '../../components/ShowResults.vue'
import SelectLeague from '../../components/SelectLeague.vue'
import SelectPosition from '../../components/SelectPosition.vue'
import axios from 'axios'

const league = ref(null)
const position = ref(null)
const maxPosition = ref(null)
const leaguesCountries = {
    "LaLiga": "Spain",
    "Premier League": "England",
    "Serie A": "Italy",
    "Bundesliga": "Germany",
    "Ligue 1": "France"
}

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

const loadData = async () => {
    loading.value = true
    if (!league.value || !position.value) return
    const res = await axios.get("https://football-charts-backend.onrender.com/position-frequency", {
        params: {
            league_name: league.value,
            position: position.value
        }
    })
    const positionCount = res.data // {"Real Madrid": 69, "Barcelona": 68, ...}
    const n = Object.keys(positionCount).length
    const colors = []
    for (let i = 1; i <= n; i++) {
        colors.push(`hsl(120, ${Math.floor(i/(n+1)*100)}%, ${Math.floor(i/(n+1)*100)}%)`)
    }

    const chartData = Object.entries(positionCount).sort((a, b) => b[1] - a[1]).map(([name, y]) => ({name, y})) // Object.entries devuelve una lista de pares de la forma [key, value]
    
    let positionOrdinal
    if (position.value == 1) {
        positionOrdinal = 'st'
    } else if (position.value == 2) {
        positionOrdinal = 'nd'
    } else if (position.value == 3) {
        positionOrdinal = 'rd'
    } else {
        positionOrdinal = 'th'
    }

    loading.value = false
    chartKey.value++ // cada vez que se pulsa el botón, se genera un gráfico con una key distinta
    chartOptions.value = {
        title: {
            text: ''
        },
        chart: {
            backgroundColor: '#eeeeee',
            type: 'pie',
            height: 600,
            // width: 1000
        },
        colors: colors,
        plotOptions: {
            pie: {
                // size: 500,
                dataLabels: {
                    enabled: true,
                    useHTML: true,
                    style: {
                        fontFamily: 'Inter'
                    },
                    formatter: function() {
                        return `<div class="row no-wrap items-center" style="font-size: 11px"><img src="https://raw.githubusercontent.com/dldelpino/football-charts/refs/heads/main/public/icons/teams/${leaguesCountries[league.value]}/${this.point.name}.png" style="width: 16px; margin-right: 6px">${this.point.name} (${this.point.y}) &#8203 &#8203 &#8203 &#8203 &#8203</div>` // &#8203 añade espacio en blanco
                    }
                }
            }
        },
        series: [{
            name: `Times finished ${position.value}${positionOrdinal}`,
            data: chartData
        }],
        credits: {
            enabled: false // elimina la marca de agua
        },
    }
}

watch(league, () => {
    position.value = null
})

watch(league, (newLeague) => {
    if (newLeague == "Bundesliga") {
        maxPosition.value = 18
    } else {
        maxPosition.value = 20
    }
})

watch(position, () => {
    if (position.value > maxPosition.value) {
        position.value = maxPosition.value
    } else if (!(position.value == null) && position.value < 1) {
        position.value = 1
    }
})

</script>

<style>

.buttons-container {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin-top: 30px;
    background-color: inherit;
    flex-wrap: wrap;
}

.chart-container {
    width: 90%;
}

.select {
    width: 200px;
}

</style>