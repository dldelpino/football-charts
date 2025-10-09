<template>
    <q-select outlined rounded label="League" :options="leagueOptions" bg-color="white" dense color="secondary" style="width: 200px;" />
</template>

<script setup>

const leagueOptions = ["LaLiga", "Premier League", "Serie A", "Bundesliga", "Ligue 1"]

</script>

<style>

.q-field--rounded .q-field__control { /* cambia el radio que aplica rounded */
    border-radius: 10px !important;
}

</style>