<template>
    <div class="buttons-container">
        <SelectLeague v-model="league"/>
        <ShowResults @click="loadData"/>
    </div>
    <div class="buttons-container" style="padding-bottom: 30px">
        <q-spinner-puff style="margin-top: 50px" v-if="loading" color="green-10" size="50px" :thickness="10"/>
        <Chart v-if="!loading" :key="chartKey" :options="chartOptions"></Chart>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { Chart } from 'highcharts-vue'
import ShowResults from '../../components/ShowResults.vue'
import SelectLeague from '../../components/SelectLeague.vue'

const league = ref(null)
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
    if (!league.value) return
    const res = await axios.get("https://football-charts-backend.onrender.com/promotion-frequency", {
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

    loading.value = false
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
            name: 'Times promoted',
            data: chartData,
            pointWidth: 20,
        }],
        credits: {
            enabled: false // elimina la marca de agua
        },
    }
}

// function loadData() {
//     fetch(`data/${league.value.toLowerCase().replace(/\s+/g, "_")}.csv`)
//         .then(response => response.text())
//         .then(csvText => {
//             Papa.parse(csvText, {
//                 header: true,
//                 complete: results => {
//                     chartKey.value++ // cada vez que se pulsa el botón, se genera un gráfico con una key distinta
//                     const seasons = []
//                     for (let i = 0; i < 25; i++) {
//                         const year1 = String(i).padStart(2, "0")
//                         const year2 = String(i+1).padStart(2, "0")
//                         seasons.push(`${year1}/${year2}`)
//                     }

//                     const promotionCount = {}

//                     for (let i = 0; i < 25; i++) {
//                         if (i == 0) {
//                             if (league.value == "LaLiga") {
//                                 promotionCount["Villarreal"] = 1
//                                 promotionCount["Las Palmas"] = 1 
//                                 promotionCount["Osasuna"] = 1
//                             } else if (league.value == "Premier League") {
//                                 promotionCount["Ipswich Town"] = 1
//                                 promotionCount["Charlton Ath"] = 1
//                                 promotionCount["Manchester City"] = 1
//                             } else if (league.value == "Serie A") {
//                                 promotionCount["Atalanta"] = 1
//                                 promotionCount["Vicenza"] = 1
//                                 promotionCount["Napoli"] = 1
//                             } else if (league.value == "Bundesliga") {
//                                 promotionCount["Köln"] = 1
//                                 promotionCount["Energie Cottbus"] = 1
//                                 promotionCount["Bochum"] = 1
//                             } else if (league.value == "Ligue 1") {
//                                 promotionCount["Lille"] = 1
//                                 promotionCount["Guingamp"] = 1
//                                 promotionCount["Toulouse"] = 1
//                             }
//                         } else {
//                             const season0 = seasons[i-1]
//                             const season1 = seasons[i]
//                             const teams0 = []
//                             const teams1 = []
//                             results.data.forEach(row => {
//                                 if (row["Season"] == season0) {
//                                     teams0.push(row["Team"])
//                                 } else if (row["Season"] == season1) {
//                                     teams1.push(row["Team"])
//                                 }
//                             })
//                             const season1Promoted = teams1.filter(team => !teams0.includes(team))
//                             season1Promoted.map(team => {
//                                 promotionCount[team] = (promotionCount[team] || 0) + 1
//                             })
//                         }
//                     }

//                     const chartData = Object.entries(promotionCount).sort((a, b) => b[1] - a[1]).map(([name, y]) => ({name, y}))

//                     const n = chartData[0].y
//                     chartData.forEach(item => {
//                         item.name = `<div class="row no-wrap items-center" style="font-size: 11px;">${item.name}<img src="https://raw.githubusercontent.com/dldelpino/football-charts/refs/heads/main/public/icons/teams/${league.value}/${item.name}.png" style="width: 16px; margin-left: 6px;"></div>`
//                         item.color = `hsl(120, ${(1-item.y/(n+1))*100}%, ${(1-item.y/(n+1))*100}%)`
//                     })

//                     chartOptions.value = {
//                         title: {
//                             text: ''
//                         },
//                         chart: {
//                             backgroundColor: '#eeeeee',
//                             type: 'bar',
//                             height: 30*chartData.length,
//                             width: 800,
//                             marginRight: 20
//                         },
//                         legend: {
//                             enabled: false
//                         },
//                         xAxis: {
//                             type: 'category',
//                             labels: {
//                                 useHTML: true
//                             }
//                         },
//                         yAxis: {
//                             max: n,
//                             title: '',
//                             labels: {
//                                 enabled: false
//                             }
//                         },
//                         plotOptions: {
//                             bar: {
//                                 dataLabels: {
//                                     enabled: true,
//                                     overflow: 'allow',
//                                     crop: false,
//                                     style: {
//                                         fontFamily: 'Inter'
//                                     }
//                                 }
//                             }
//                         },
//                         series: [{
//                             name: 'Times promoted',
//                             data: chartData,
//                             pointWidth: 20,
//                         }],
//                         credits: {
//                             enabled: false // elimina la marca de agua
//                         },
//                     }
//                 }
//             })
//         })
// }

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