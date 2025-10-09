<template>
  <div></div>
</template>

<script setup>

import { onMounted } from 'vue'

onMounted(() => {
  fetch("https://football-charts-backend.onrender.com/")
    .then(() => {console.log("Backend loaded successfully")})
    .catch(() => console.warn("Loading backend failed"))
})

</script>

<style>

</style>