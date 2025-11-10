<template>
    <q-dialog>
        <q-card class="card">
            <q-card-section>
                <div class="text-h4" style="font-weight: bold">Error</div>
            </q-card-section>

            <q-card-section>
                <div class="text-h6" style="font-weight: normal">There is no data available for this selection. Try changing the parameters.</div>
            </q-card-section>

            <q-card-actions align="right">
                <q-btn flat label="OK" color="secondary" style="font-weight: bold" v-close-popup />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script setup>

</script>

<style lang="scss">

.card {
    border: 2px solid $secondary;
    border-radius: 10px !important;
    padding: 10px
}

</style>