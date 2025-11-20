<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>

        <q-input v-model.number="position" :disable="!league" outlined rounded bg-color="white" dense color="secondary" style="width: 110px;" label="Pos.">
            <template v-slot:append>
                <q-btn round dense flat icon="remove" size="10px" @mousedown="decreasePosition" @mouseup="clear" @mouseleave="clear"/>
                <q-btn round dense flat icon="add" size="10px" @mousedown="increasePosition" @mouseup="clear" @mouseleave="clear"/>
            </template>
        </q-input>

        <ShowResults @click="loadData"/>
    </div>
    <div class="data-container">
        <LoadingSpinner v-if="loading"/>
        <LoadingMessage :class="{visible: showMessage}"/>
        <div style="width: 90%">
            <Chart v-if="!loading" :key="chartKey" :options="chartOptions"></Chart>
        </div>
    </div>
</template>

<script setup>

import { ref, watch } from 'vue'
import { Chart } from 'highcharts-vue'
import axios from 'axios'

import LoadingMessage from 'src/components/LoadingMessage.vue'
import LoadingSpinner from 'src/components/LoadingSpinner.vue'
import SelectLeague from '../../components/SelectLeague.vue'
import ShowResults from '../../components/ShowResults.vue'

const league = ref(null)
const position = ref(null)
const maxPosition = ref(null)

let interval = null
let timeout = null

const decreasePosition = () => {
    position.value--
    timeout = setTimeout(() => {
        interval = setInterval(() => position.value--, 50)
    }, 250)
}
const increasePosition = () => {
    position.value++
    timeout = setTimeout(() => {
        interval = setInterval(() => position.value++, 50)
    }, 250)
}
const clear = () => {
    clearInterval(interval)
    clearTimeout(timeout)
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
    if (!league.value || !position.value) return

    loading.value = true
    const timeout = setTimeout(() => {
        showMessage.value = true
    }, 10000)

    const res = await axios.get("https://football-charts-backend.onrender.com/position-frequency", {
        params: {
            league_name: league.value,
            position: position.value
        }
    })

    const positionCount = res.data // {"Real Madrid": 69, "Barcelona": 68, ...}
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

    const n = Object.keys(positionCount).length
    const colors = []
    for (let i = 1; i <= n; i++) {
        colors.push(`hsl(120, ${Math.floor(i/(n+1)*100)}%, ${Math.floor(i/(n+1)*100)}%)`)
    }

    clearTimeout(timeout)
    loading.value = false
    showMessage.value = false

    chartKey.value++ // cada vez que se pulsa el botón, se genera un gráfico con una key distinta

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
    } else if (newLeague == "LaLiga2") {
        maxPosition.value = 22
    } else {
        maxPosition.value = 20
    }
})

watch(position, (newPosition) => {
    if (newPosition > maxPosition.value) position.value = maxPosition.value
    else if (!(position.value == null) && position.value < 1) position.value = 1
})

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