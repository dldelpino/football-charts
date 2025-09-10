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
import { Chart } from 'highcharts-vue'
import Papa from 'papaparse'
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

function loadData() {
    fetch(`data/${league.value.toLowerCase().replace(/\s+/g, "_")}.csv`)
        .then(response => response.text())
        .then(csvText => {
            Papa.parse(csvText, {
                header: true,
                complete: results => {
                    chartKey.value++ // cada vez que se pulsa el botón, se genera un gráfico con una key distinta
                    const seasons = []
                    for (let i = 0; i < 25; i++) {
                        const year1 = String(i).padStart(2, "0")
                        const year2 = String(i+1).padStart(2, "0")
                        seasons.push(`${year1}/${year2}`)
                    }

                    const relegationCount = {}

                    for (let i = 24; i >= 0; i--) {
                        if (i == 24) {
                            if (league.value == "LaLiga") {
                                relegationCount["Leganés"] = 1
                                relegationCount["Las Palmas"] = 1 
                                relegationCount["Valladolid"] = 1
                            } else if (league.value == "Premier League") {
                                relegationCount["Leicester City"] = 1
                                relegationCount["Ipswich Town"] = 1
                                relegationCount["Southampton"] = 1
                            } else if (league.value == "Serie A") {
                                relegationCount["Empoli"] = 1
                                relegationCount["Venezia"] = 1
                                relegationCount["Monza"] = 1
                            } else if (league.value == "Bundesliga") {
                                relegationCount["Holstein Kiel"] = 1
                                relegationCount["Bochum"] = 1
                            } else if (league.value == "Ligue 1") {
                                relegationCount["Reims"] = 1
                                relegationCount["Saint-Étienne"] = 1
                                relegationCount["Montpellier"] = 1
                            }
                        } else {
                            const season0 = seasons[i]
                            const season1 = seasons[i+1]
                            const teams0 = []
                            const teams1 = []
                            results.data.forEach(row => {
                                if (row["Season"] == season0) {
                                    teams0.push(row["Team"])
                                } else if (row["Season"] == season1) {
                                    teams1.push(row["Team"])
                                }
                            })
                            const season1Relegated = teams0.filter(team => !teams1.includes(team))
                            season1Relegated.map(team => {
                                relegationCount[team] = (relegationCount[team] || 0) + 1
                            })
                        }
                    }

                    const chartData = Object.entries(relegationCount).sort((a, b) => b[1] - a[1]).map(([name, y]) => ({name, y}))

                    const n = chartData[0].y
                    chartData.forEach(item => {
                        item.name = `<div class="row no-wrap items-center" style="font-size: 11px">${item.name}<img src="https://raw.githubusercontent.com/dldelpino/football-charts/refs/heads/main/public/icons/teams/${league.value}/${item.name}.png" style="width: 16px; margin-left: 6px"></div>`
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
                            name: 'Times promoted',
                            data: chartData,
                            pointWidth: 20,
                        }],
                        credits: {
                            enabled: false // elimina la marca de agua
                        },
                    }
                }
            })
        })
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