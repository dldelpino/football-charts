<template>
    <div class="loading-message">The first data load may take up to one minute.</div>
</template>

<script setup>

</script>

<style lang="scss">

.loading-message {
    text-align: center;
    margin-top: 20px;
    color: $secondary;
    opacity: 0;
    visibility: hidden;
    transition: opacity 0.5s ease, visibility 0s;
}

.loading-message.visible {
    opacity: 1;
    visibility: visible;
    transition: opacity 0.5s ease
}

</style>