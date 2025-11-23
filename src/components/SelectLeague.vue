<template>
    <q-select outlined rounded label="League" :options="options" bg-color="white" dense color="secondary" style="width: 170px;">
        <template v-slot:option="scope">
            <q-item v-bind="scope.itemProps">
                <div style="display: flex; align-items: center; gap: 8px">
                    <img :src="`icons/flags/${leagueCountry[scope.opt]}.png`" width="16px"/>
                    {{ scope.opt}}
                </div>
            </q-item>
        </template>
        <template v-slot:selected-item="scope">
            {{ scope.opt}}
        </template>
    </q-select>
</template>

<script setup>

import { inject } from 'vue'

const leagueCountry = inject('leagueCountry')

const options = Object.keys(leagueCountry)

</script>

<style>

.q-field--rounded .q-field__control { /* cambia el radio que aplica rounded */
    border-radius: 10px !important;
}

</style>