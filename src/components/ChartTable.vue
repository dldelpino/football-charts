<template>
    <q-table class="stats-table" flat bordered virtual-scroll hide-bottom :rows-per-page-options="[0]">
        <template v-slot:body-cell-team="props">
            <q-td :props="props" style="align-items: center" class="row">
                <img :src="props.row.logo" style="width: 16px; margin-right: 8px"/>
                {{ props.row.team }}
            </q-td>
        </template>
    </q-table>
</template>

<script setup>

</script>

<style>

.stats-table, .stats-table th, .stats-table td {
    border-color: #c2c2c2;
}

.stats-table {
    border-radius: 10px;
    max-width: 90%;
    font-feature-settings: "tnum";
}

</style>