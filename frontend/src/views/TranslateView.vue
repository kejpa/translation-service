<script setup>

</script>

<template>
  <div class="translate-view">
    <h1>Translate Document</h1>

    <div class="card">
      <label>
        Source document

        <input
          type="file"
          accept=".docx"
          @change="onSourceFileChanged"
        >
      </label>

      <label>
        Output filename

        <input
          v-model="outputFilename"
          type="text"
          placeholder="translated.docx"
        >
      </label>

      <div class="actions">
        <button
          type="button"
          @click="clearForm"
        >
          Clear
        </button>

        <button
          type="button"
          :disabled="!canTranslate"
        >
          Translate
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const sourceFile = ref(null)

const outputFilename = ref(
  'translated.docx',
)

function onSourceFileChanged(event) {
  sourceFile.value =
    event.target.files?.[0] ?? null
}

function clearForm() {
  sourceFile.value = null
  outputFilename.value =
    'translated.docx'
}

const canTranslate = computed(
  () => sourceFile.value !== null,
)
</script>

<style scoped>
.translate-view {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card {
  display: flex;
  flex-direction: column;
  gap: 1rem;

  padding: 1rem;

  border: 1px solid
    var(--color-border);

  border-radius: 0.5rem;

  background:
    var(--color-surface);
}

label {
  display: flex;
  flex-direction: column;

  gap: 0.5rem;

  font-weight: 600;
}

input[type='text'] {
  padding: 0.5rem;

  border: 1px solid
    var(--color-border);

  background:
    var(--color-background);

  color: var(--color-text);
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
