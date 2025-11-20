<template>
    <q-select outlined rounded label="League" :options="leagueOptions" bg-color="white" dense color="secondary" style="width: 170px;">
        <template v-slot:option="scope">
            <q-item v-bind="scope.itemProps">
                <div style="display: flex; align-items: center; gap: 8px">
                    <img :src="`icons/flags/${leagueCountries[scope.opt]}.png`" width="16px"/>
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

const leagueCountries = {
    "LaLiga": "Spain",
    "LaLiga2": "Spain",
    "Premier League": "England",
    "Serie A": "Italy",
    "Bundesliga": "Germany",
    "Ligue 1": "France"
}
const leagueOptions = ["LaLiga", "LaLiga2", "Premier League", "Serie A", "Bundesliga", "Ligue 1"]

</script>

<style>

.q-field--rounded .q-field__control { /* cambia el radio que aplica rounded */
    border-radius: 10px !important;
}

</style>