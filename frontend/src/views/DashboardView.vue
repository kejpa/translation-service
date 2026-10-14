<script setup>
import DashboardCard from '@/components/DashboardCard.vue'
import ModelCard from '@/components/ModelCard.vue'
import {useDashboardStore} from "@/stores/dashboardStore.js";
import {storeToRefs} from "pinia";
import {computed, onMounted} from "vue";

const dashboardStore = useDashboardStore()
const {loading, health, configuration, configurationData, translationMemory} = storeToRefs(dashboardStore)
const modelAvailable = computed(
  () => configurationData.value?.model_available,
)

const configuredModel = computed(
  () => configurationData.value?.model,
)

onMounted(() => {
  dashboardStore.getDashboard()
})
</script>

<template>
  <h1>Dashboard</h1>
  <div class="dashboard">
    <DashboardCard :data="health" title="Service Status"/>

    <DashboardCard v-if="modelAvailable" :data="configuration" title="Ollama Configuration"/>
    <ModelCard v-else :model="configuredModel" @installed="dashboardStore.getDashboard()"/>

    <DashboardCard :data="translationMemory" title="Translation Memory"/>
  </div>
</template>


<style scoped>
.dashboard {
  display: grid;
  gap: 1rem;
}
</style>
