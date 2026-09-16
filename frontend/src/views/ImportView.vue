<script setup>
import {useImportStore} from "@/stores/importStore.js";
import {computed, ref} from "vue";
import {storeToRefs} from "pinia";

const importStore = useImportStore()
const {loading, error, result} = storeToRefs(importStore)

const sourceFileInput = ref(null)
const targetFileInput = ref(null)

const canImport = computed(() =>
  importStore.sourceFile !== null &&
  importStore.targetFile !== null &&
  !importStore.loading,
)

function clearForm() {
  importStore.clear()

  sourceFileInput.value.value = ''
  targetFileInput.value.value = ''
}

function onSourceFileChanged(event) {
  importStore.setSourceFile(
    event.target.files[0],
  )
}

function onTargetFileChanged(event) {
  importStore.setTargetFile(
    event.target.files[0],
  )
}
</script>
<template>
  <div class="import-view">
    <h1>Import document pair</h1>

    <div class="card">
      <div class="form-group">
        <label>
          Source document (fi)

          <input
            ref="sourceFileInput"
            accept=".docx"
            type="file"
            @change="onSourceFileChanged"
          />
        </label>
      </div>

      <div class="form-group">
        <label>
          Target document (sv)


          <input
            ref="targetFileInput"
            accept=".docx"
            type="file"
            @change="onTargetFileChanged"
          />
        </label>
      </div>

      <div class="actions">
        <button
          :disabled="!canImport || importStore.loading"
          @click="importStore.importDocuments()"
        >
          Import
        </button>

        <button
          :disabled="loading"
          type="button"
          @click="clearForm"
        >
          Clear
        </button>
      </div>
    </div>
    <div v-if="loading">
      Importing...
    </div>

    <div
      v-if="error"
      class="error-message"
    >
      <strong>Import failed</strong>

      <p>{{ error }}</p>
    </div>
    <div
      v-if="result"
      class="success-message"
    >
      <strong>Import completed successfully</strong>

      <div class="result-row">
        <span>Source document</span>
        <span>{{ result.source_document }}</span>
      </div>

      <div class="result-row">
        <span>Target document</span>
        <span>{{ result.target_document }}</span>
      </div>

      <div class="result-row">
        <span>Imported segments</span>
        <span>{{ result.imported_segments }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.import-view {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card {
  padding: 1rem;

  border: 1px solid var(--color-border);
  border-radius: 0.5rem;

  background: var(--color-surface);
}

.form-group {
  display: flex;
  flex-direction: column;

  gap: 0.5rem;
  margin-bottom: 1rem;
}

label {
  font-weight: 600;
}


input[type="file"] {
  color: var(--color-text);
}

.actions {
  display: flex;
  justify-content: flex-end;
}

button {
  margin-left: 0.5rem;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;

  border: 1px solid #c00000;

  background: #ffeaea;
}

.success-message {
  margin-top: 1rem;
  padding: 1rem;

  border: 1px solid var(--color-border);
  background: var(--color-surface);
}

.result-row {
  display: grid;
  grid-template-columns: 200px 1fr;

  padding: 0.4rem;
}

.result-row:nth-child(even) {
  background: var(--color-surface-alternating);
}
</style>
