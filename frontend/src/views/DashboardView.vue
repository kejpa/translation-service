<script setup>
import DashboardCard from '@/components/DashboardCard.vue'
import {useDashboardStore} from "@/stores/dashboardStore.js";
import {storeToRefs} from "pinia";
import {onMounted} from "vue";

const dashboardStore = useDashboardStore()
const {loading, health, configuration, translationMemory} = storeToRefs(dashboardStore)

onMounted(() => {
  dashboardStore.getDashboard()
})
</script>

<template>
  <h1>Dashboard</h1>
  <div class="dashboard">
    <DashboardCard :data="health" title="Service Status"/>

    <DashboardCard :data="configuration" title="Translation Configuration"/>

    <DashboardCard :data="translationMemory" title="Translation Memory"/>
  </div>
</template>


<style scoped>
.dashboard {
  display: grid;
  gap: 1rem;
}
</style>
