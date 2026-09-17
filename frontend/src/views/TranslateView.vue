<script setup>
import {computed, ref} from 'vue'
import {useTranslateStore} from '@/stores/translateStore'
import {storeToRefs} from "pinia";

const translateStore = useTranslateStore()
const {sourceFile, outputFilename, loading, error} = storeToRefs(translateStore)
const sourceFileInput = ref(null)

function onSourceFileChanged(event) {
  translateStore.setSourceFile(
    event.target.files?.[0] ?? null,
  )
}

function clearForm() {
  translateStore.clear()

  if (sourceFileInput.value) {
    sourceFileInput.value.value = ''
  }
}

const canTranslate = computed(
  () =>
    sourceFile.value !== null &&
    !loading.value,
)
</script>

<template>
  <div class="translate-view">
    <h1>Translate Document</h1>

    <div class="card">
      <label>
        Source document

        <input
          ref="sourceFileInput"
          accept=".docx"
          type="file"
          @change="onSourceFileChanged"
        >
      </label>

      <label>
        Output filename

        <input
          v-model="outputFilename"
          placeholder="translated.docx"
          type="text"
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
          :disabled="!canTranslate"
          type="button"
          @click="translateStore.translateDocument()"
        >
          Translate
        </button>
      </div>
    </div>
  </div>
</template>

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

input[type='text'] {
  padding: 0.5rem;

  border: 1px solid var(--color-border);

  background: var(--color-background);

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
