<script setup>
import {computed, ref} from 'vue'
import {useTranslateStore} from '@/stores/translateStore'
import {storeToRefs} from "pinia";
import DashboardCard from "@/components/DashboardCard.vue";
import {objectToRows} from "@/utils/objectToRows.js";

const statisticsLabelMap = {
  total_paragraphs: 'Total Paragraphs',
  translated: 'Translated',
  fuzzy_high: 'Fuzzy High',
  fuzzy_low: 'Fuzzy Low',
  llm: 'LLM',
  missing: 'Missing',
  empty: 'Empty',
}

const translateStore = useTranslateStore()
const {sourceFile, outputFilename, loading, result, error} = storeToRefs(translateStore)

const sourceFileInput = ref(null)
const canTranslate = computed(
  () =>
    sourceFile.value !== null &&
    !loading.value,
)

const statistics = computed(() => {
  if (!translateStore.result) {
    return null
  }

  return objectToRows(
    result.value.statistics,
    statisticsLabelMap,
  )
})

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

function downloadResult() {
  window.location.href =
    import.meta.env.VITE_API_BASE_URL +
    translateStore.result.download_url
}
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
          :disabled="!canTranslate"
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
          {{
            loading
              ? 'Translating...'
              : 'Translate'
          }}
        </button>
      </div>
    </div>
  </div>
  <div
    v-if="loading"
    class="info-message"
  >
    Translating document...
  </div>
  <div
    v-if="result"
    class="success-message"
  >
    <strong>
      Translation completed successfully
    </strong>
  </div>
  <DashboardCard
    v-if="statistics"
    :data="statistics"
    title="Translation Statistics"
  />
  <div
    v-if="result"
    class="actions"
  >
    <button
      type="button"
      @click="downloadResult"
    >
      Download translated document
    </button>
  </div>
  <div
    v-if="error"
    class="error-message"
  >
    <strong>
      Translation failed
    </strong>

    <p>
      {{ error }}
    </p>
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

.success-message,
.error-message,
.info-message {
  padding: 1rem;
  margin-top: 1rem;

  border: 1px solid var(--color-border);

  background: var(--color-surface);
}

.success-message {
  border-left: 4px solid green;
}

.error-message {
  border-left: 4px solid red;
}

.info-message {
  border-left: 4px solid blue;
}
</style>
