<template>
    <q-input v-model.number="number" outlined rounded bg-color="white" dense color="secondary" style="width: 110px;">
        <template v-slot:append>
            <q-btn round dense flat icon="remove" size="10px" @mousedown="decreaseNumber" @mouseup="clear" @mouseleave="clear"/>
            <q-btn round dense flat icon="add" size="10px" @mousedown="increaseNumber" @mouseup="clear" @mouseleave="clear"/>
        </template>
    </q-input>
</template>

<script setup>

const number = defineModel()

let interval = null
let timeout = null

const decreaseNumber = () => {
    number.value--
    timeout = setTimeout(() => {
        interval = setInterval(() => number.value--, 50)
    }, 250)
}

const increaseNumber = () => {
    number.value++
    timeout = setTimeout(() => {
        interval = setInterval(() => number.value++, 50)
    }, 250)
}

const clear = () => {
    clearInterval(interval)
    clearTimeout(timeout)
}

</script>

<style>



</style>