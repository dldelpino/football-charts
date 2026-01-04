<template>
    <q-table class="stats-table" flat bordered virtual-scroll :hide-bottom="!props.legend.length" :rows-per-page-options="[-1]">
        <template v-slot:body-cell-status="tableProps">
            <q-td :props="tableProps" :style="tableProps.row.status >= 11 ?
                {background: `linear-gradient(to bottom, ${props.legend.find(item => item.key == tableProps.row.status)?.color} 50%, #bf2a2a 50%)`} :
                {backgroundColor: props.legend.find(item => item.key == tableProps.row.status)?.color}"
            />
        </template>

        <template v-slot:body-cell-team="tableProps">
            <q-td :props="tableProps" style="align-items: center" class="row">
                <img :src="tableProps.row.logo" style="width: 16px; margin-right: 8px"/>
                {{ tableProps.row.team }}
            </q-td>
        </template>

        <template v-slot:bottom v-if="props.legend.length">
            <div class="row" style="gap: 16px; flex-wrap: wrap"> <!-- si uso q-td aparecen bordes raros -->
                <div v-for="item in filteredLegend" :key="item.key" class="flex items-center" style="gap: 6px">
                    <div :style="{backgroundColor: item.color, width: '10px', height: '10px', borderRadius: '2px'}"></div>
                    {{ item.label }}
                </div>
                <div v-if="filteredLegend.some(item => item.key == 11 || item.key == 12)" class="flex items-center" style="gap: 6px">
                    <div :style="{backgroundColor: '#bf2a2a', width: '10px', height: '10px', borderRadius: '2px'}"></div>
                    Relegation
                </div>
            </div>
        </template>
    </q-table>
</template>

<script setup>

import { computed } from 'vue'

const props = defineProps({
    legend: { type: Array, default: () => [] }
})

const filteredLegend = computed(() => 
    props.legend.filter(item => {
        if (props.legend.some(otherItem => otherItem.key == 11) && (item.key == 2 || item.key == 7)) 
            return false
        else if (props.legend.some(otherItem => otherItem.key == 12) && (item.key == 3 || item.key == 7)) 
            return false
        else
            return true
    })
)

</script>

<style>

.stats-table, .stats-table th, .stats-table td {
    border-color: #c2c2c2;
}

.q-table__bottom {
    box-shadow: inset 0 2px 0 0 #e1e1e1; /* chanchullo para duplicar el borde superior de la fila de la leyenda*/
}

.stats-table {
    border-radius: 10px;
    max-width: 90%;
    font-feature-settings: "tnum";
}

</style>