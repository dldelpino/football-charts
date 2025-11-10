<template>
    <q-input v-model.number="number" outlined rounded bg-color="white" dense color="secondary" style="width: 110px">
        <template v-slot:append>
            <q-btn 
                round 
                dense 
                flat 
                icon="remove" 
                size="10px" 
                @mousedown="decrease"
                @mouseup="clear"
                @mouseleave="clear"
            />
            <q-btn 
                round 
                dense 
                flat 
                icon="add" 
                size="10px" 
                @mousedown="increase"
                @mouseup="clear"
                @mouseleave="clear"
            />
        </template>
    </q-input>
</template>

<script setup>

import { ref } from 'vue'

const number = ref(null)

let interval = null
let timeout = null

const decrease = () => {
    number.value--
    timeout = setTimeout(() => {
        interval = setInterval(() => number.value--, 50)
    }, 250)
}

const increase = () => {
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