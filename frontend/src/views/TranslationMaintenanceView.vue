<script setup>
import {useTranslationMemoryStore} from '@/stores/translationMemoryStore'
import {storeToRefs} from "pinia";

const translationMemoryStore = useTranslationMemoryStore()
const {query, translationUnits, loading, error, selectedUnit,} = storeToRefs(translationMemoryStore)

function confirmDelete() {
  if (
    window.confirm(
      'Delete translation unit?',
    )
  ) {
    translationMemoryStore.remove()
  }
}
</script>
<template>
  <div class="translation-memory-view">
    <h1>Translation Memory</h1>

    <div class="card">
      <label>
        Search

        <input
          v-model="query"
          placeholder="Search source text..."
          type="text"
        >
      </label>
      <div class="actions">
        <button
          type="button"
          @click="translationMemoryStore.search()"
        >
          Search
        </button>
      </div>
    </div>
    <div
      v-if="loading"
      class="info-message"
    >
      Searching...
    </div>
    <div
      v-if="error"
      class="error-message"
    >
      {{ error }}
    </div>
    <div
      v-if="selectedUnit"
      class="card"
    >
      <h2>Edit Translation Unit</h2>

      <label>
        Source text

        <textarea
          v-model="
        selectedUnit.source_text
      "
          rows="4"
        />
      </label>

      <label>
        Target text

        <textarea
          v-model="
        selectedUnit.target_text
      "
          rows="4"
        />
      </label>

      <div class="actions">
        <button
          type="button"
          @click="translationMemoryStore.update()"
        >
          Save
        </button>
        <button
          type="button"
          @click="confirmDelete"
        >
          Delete
        </button>
      </div>
    </div>

    <div class="card">
      <table>
        <thead>
        <tr>
          <th>ID</th>
          <th>Source Text</th>
          <th>Target Text</th>
        </tr>
        </thead>

        <tbody>
        <tr
          v-for="unit in translationUnits"
          :key="unit.id"
          :class="{ 'selected': unit.id === selectedUnit?.id }"
          @click="translationMemoryStore.selectUnit(unit)"
        >
          <td>{{ unit.id }}</td>

          <td>{{ unit.source_text }}</td>

          <td>{{ unit.target_text }}</td>
        </tr>
        <tr
          v-if="
      !loading &&
      translationUnits.length === 0
    "
        >
          <td colspan="3">
            No translation units found.
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.translation-memory-view {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

button {
  margin-left: 0.5rem;
}

.card {
  padding: 1rem;

  border: 1px solid var(--color-border);
  border-radius: 0.5rem;

  background: var(--color-surface);
}

label {
  display: flex;
  flex-direction: column;

  gap: 0.5rem;

  font-weight: 600;
}

input {
  padding: 0.5rem;

  border: 1px solid var(--color-border);

  background: var(--color-background);
  color: var(--color-text);
}

.actions {
  display: flex;
  justify-content: flex-end;

  margin-top: 1rem;
}

table {
  width: 100%;

  border-collapse: collapse;
}

th,
td {
  padding: 0.5rem;

  text-align: left;
}

thead {
  border-bottom: 1px solid var(--color-border);
}

tbody tr {
  cursor: pointer;
}

tbody tr:hover {
  background: var(--color-surface-alternating);
}

tbody tr:nth-child(even) {
  background: var(--color-surface-alternating);
}

.selected {
  background: var(--color-surface-highlighted) !important;
}
</style>
