<script setup>
import { RouterView } from 'vue-router'
import AppMenu from './components/AppMenu.vue'
</script>

<template>
  <div class="app-layout">
    <AppMenu />

    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 1rem;

  min-height: 100vh;
}

.content {
  padding: 1rem;
}
</style>
