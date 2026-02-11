<template>
  <div style="display: flex; align-items: center; justify-content: center; height: 540px;">
    <q-card flat bordered class="stats-card">
      <Transition name="fade" mode="out-in">
        <div v-if="groupNumber !== null" :key="statNumber">
          {{ console.log(statParser(randomStats[groupNumber][statNumber])) }}
          <template v-for="(x, i) in statParser(randomStats[groupNumber][statNumber])" :key="i">
            <span v-if="x.type == 'text'">
              {{ x.value }}
            </span>
            <span v-else>
              <img 
                :src="`icons/teams/${x.team}.png`" 
                :style="[
                  {width: '16px'},
                  {marginRight: '3px'},
                  {verticalAlign: 'middle'},
                  {paddingBottom: '4px'},
                  i > 0 ? {marginLeft: '3px'} : {}
                ]"
              />
              {{ x.value }}
            </span>
          </template>
        </div>
      </Transition>
      <q-btn flat rounded dense size="13px" class="bg-white" text-color="secondary" style="font-weight: bold; width: 60px; align-self: flex-end; margin-top: 10px" label="Next" @click="nextStat"/>
    </q-card>
  </div>
</template>

<script setup>

import { ref, onMounted } from 'vue'
import randomStats from 'src/random_stats.json'

const keys = Object.keys(randomStats)

const groupNumber = ref(null)
const statNumber = ref(null)

const nextStat = () => {
  let newGroupNumber = Math.floor(Math.random() * keys.length) // inicializo con el mismo valor para que el bucle se ejecute al menos una vez
  while (newGroupNumber == groupNumber.value) { // necesito que el grupo dela nueva stat sea diferente de la anterior
    newGroupNumber = Math.floor(Math.random() * keys.length)
  }
  groupNumber.value = newGroupNumber
  statNumber.value = Math.floor(Math.random() * randomStats[groupNumber.value].length)
}

const statParser = (stat) => { // en esta parte me ha echado un cable ChatGPT porque no me apetece estudiar expresiones regulares
  const result = []
  const i = stat.match(/\s(is|are)\s/).index
  const part1 = stat.slice(0, i)
  const part2 = stat.slice(i)
  const regex = /.*?(?:\([^)]*\))?(?:,\s+| and |$)/g 
  // la idea es convertir "Equipo 1 (14/15), Equipo 2 y Equipo 3 (LaLiga)" en ["Equipo 1 (14/15), ", "Equipo 2 y ", "Equipo 3"]
  for (const x of part1.match(regex)) {
    if (x.trim()) {
      const teamName = x
        .replace(/\s*\([^)]*\)/, '') // nombre limpio para el icono
        .replace(/,\s*$|\s+and\s*$/, '') // quitamos el separador solo para el nombre
        .trim()
      result.push({
        type: 'team',
        team: teamName,
        value: x
      })
    }
  }
  result.push(
    {
      type: 'text',
      value: part2
    }
  )
  return result
}

onMounted(() => {
  nextStat()
  fetch("https://football-charts-backend.onrender.com/")
    .then(() => {console.log("Backend loaded successfully")})
    .catch(() => console.warn("Loading backend failed"))
})

</script>

<style>

.q-btn--rounded { /* cambia el radio que aplica rounded a los botones */
    border-radius: 10px !important;
}

.q-card { /* cambia el radio que aplica rounded a los botones */
    border-radius: 10px !important;
    border-color: #c2c2c2;
}

.fade-enter-active, /* https://vuejs.org/guide/built-ins/transition.html#transition-between-elements */ 
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.stats-card {
  width: 600px;
  display: flex;
  flex-direction: column;
  padding: 15px;
  justify-content: space-between;
}

</style>