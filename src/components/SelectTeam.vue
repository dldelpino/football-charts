<template>
    <q-select v-model="team" :disable="!league" :options="options" outlined rounded bg-color="white" size="100px" dense color="secondary" style="width: 220px" label="Team">
        <template v-slot:option="scope">
            <q-item v-bind="scope.itemProps">
                <div style="display: flex; align-items: center; gap: 8px">
                    <img :src="`icons/teams/${leagueCountry[league]}/${scope.opt}.png`" width="16px"/>
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

import { computed, inject } from 'vue'

const team = defineModel()
const league = defineModel('league')

const leagueCountry = inject('leagueCountry')
const leagueTeams = inject('leagueTeams')

const options = computed(() => {
    return league.value ? leagueTeams[league.value] : []
})

</script>

<style>

</style>