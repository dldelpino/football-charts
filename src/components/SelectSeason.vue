<template>
    <q-select outlined rounded :options="seasons" bg-color="white" dense color="secondary" style="width: 104px" label="Season"/> <!-- 104px es la anchura mínima para que quepa el texto en la caja-->
</template>

<script setup>

const seasons = []
for (let i = 0; i < 25; i++) {
    const year1 = String(i).padStart(2, "0")
    const year2 = String(i+1).padStart(2, "0")
    seasons.push(`${year1}/${year2}`)
}

</script>

<style>

.q-field--rounded .q-field__control { /* cambia el radio que aplica rounded */
    border-radius: 10px !important;
}

</style>