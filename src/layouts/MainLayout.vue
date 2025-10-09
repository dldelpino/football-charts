<template>
  <q-layout view="lHh Lpr lFf" class="bg-grey-3">
    <q-page-container>
        <div class="bg-grey-3 header">
          <div>
            <div style="font-size: 21px; font-weight: bold;">
              {{ pageTitle }}
            </div>
            <div style="color: dimgray">
              {{ pageDescription }}
            </div>
          </div>
          <div class="icons-container">
            <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />
          </div>
        </div>
        <div class="rule"></div>
    </q-page-container>

    <q-drawer v-model="leftDrawerOpen" show-if-above class="drawer">
      <q-list>
        <q-item-label header class="drawer-title">
          <q-icon :name="`img:icons/ball-white.png`" class="drawer-title-icon"/>
          Football Charts
        </q-item-label>
        <template v-for="(value, key, index) in sections" :key="index">
        <q-item-label header class="drawer-header">{{ key }}</q-item-label>
          <template v-for="(page, index) in sections[key]" :key="index">
            <q-btn flat no-caps :class="isActive(page) ? 'active-drawer-button' : 'drawer-button' " :to="'/' + toKebabCase(page)" align="left"> <!-- no sé por qué align sale en rojo -->
              <q-icon :name="`img:icons/${toKebabCase(key)}.png`" :class="isActive(page) ? 'active-drawer-icon' : 'drawer-icon' "/>
              {{ page }}
            </q-btn>
          </template>
        </template>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>

import { ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const sections = {
  'TABLES': ['Average Stats', 'Position History', 'Promoted Teams', 'Season Standings', 'Team Trajectory'],
  'PIE CHARTS': ['Position Frequency'],
  'BAR CHARTS': ['Promotion Frequency', 'Relegation Frequency'],
}

const leftDrawerOpen = ref(false)
const pageTitle = ref('')
const pageDescription = ref('')

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

function toKebabCase(str) {
  return str.toLowerCase().split(' ').join('-')
}

function isActive(item) {
  const path = '/' + toKebabCase(item)
  return route.path === path
}

watchEffect(() => { // se ejecuta cuando cambian route.meta.title o route.meta.description
  pageTitle.value = route.meta.title
  pageDescription.value = route.meta.description
})

</script>

<style lang="scss">

html {
  background-color: $grey-3;
}

.header {
  display: flex;
  color: black;
  padding-left: 20px;
  padding-right: 20px;
  padding-top: 20px;
  padding-bottom: 10px;
  justify-content: space-between;
}

.rule {
  margin-left: 20px;
  margin-right: 20px;
  border-bottom: 1px solid #c2c2c2
}

.drawer {
  display: flex;
  background: hsl(120, 26%, 18%) !important;
}

.icons-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.toolbar-icon {
  width: 25px;
  display: block;
  transition: transform 0.1s;
}

.toolbar-icon:hover {
  transform: scale(1.2);
}

.drawer-header {
  font-size: 13px;
  font-weight: 700;
  color: rgb(220, 220, 220);
}

.drawer-icon {
  width: 20px;
  height: auto;
  margin-right: 10px;
  filter: invert(95%) sepia(18%) saturate(0%) hue-rotate(179deg) brightness(88%) contrast(99%); 
  /* https://codepen.io/sosuke/pen/Pjoqqp */
}

.active-drawer-icon {
  width: 20px;
  height: auto;
  margin-right: 10px;
  filter: invert(90%) sepia(15%) saturate(914%) hue-rotate(61deg) brightness(88%) contrast(96%);
}

.drawer-button {
  font-weight: 500;
  border-radius: 10px;
  margin-left: 15px;
  margin-bottom: 15px;
  color: rgb(220, 220, 220);
  width: 89%;
}

.active-drawer-button {
  font-weight: 500;
  border-radius: 10px;
  margin-left: 15px;
  margin-bottom: 15px;
  color: rgb(150, 220, 150);
  width: 89%;
}

.drawer-title {
  display: flex;
  color: white;
  align-items: center;
  gap: 10px;
  font-weight: 700;
  font-size: 21px;
}

.drawer-title-icon {
  width: 30px;
  height: 30px;
}

</style>