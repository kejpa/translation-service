<script setup>
defineProps({
  title: String,
  data: Object,
})
</script>

<template>
  <section class="card">
    <h2>{{ title }}</h2>

    <div v-if="data">
      <div
        v-for="row in data"
        :key="row.label"
        class="row"
      >
        <span>{{ row.label }}</span>
        <span>{{ row.value }}</span>
      </div>
    </div>

    <div v-else>
      Loading...
    </div>
  </section>
</template>

<style scoped>
h2 {
  margin-bottom: 1rem;
  font-size: 1rem;
}

.card {
  padding: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 0.5rem;
  background: var(--color-surface);
}

.card h2 {
  font-size: 1rem;
  font-weight: 600;

  padding-bottom: 0.5rem;
  margin-bottom: 0.5rem;

  border-bottom: 1px solid var(--color-border);
}

.row {
  display: grid;
  grid-template-columns: 250px 1fr;

  padding: 0.4rem 0.6rem;
}

.row:nth-child(even) {
  background: var(--color-surface-alternating);
}
</style>
