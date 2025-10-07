<template>
    <q-select outlined rounded :options="leagueOptions" bg-color="white" dense color="primary" style="width: 200px;" />
</template>

<script setup>

const leagueOptions = ["LaLiga", "Premier League", "Serie A", "Bundesliga", "Ligue 1"]

</script>

<style>

.q-field--rounded .q-field__control { /* cambia el radio que aplica rounded */
    border-radius: 10px !important;
}

</style>