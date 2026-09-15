import {ref} from 'vue'
import {defineStore} from 'pinia'
import {getHealth, getTranslationMemoryStatistics} from "@/services/dashboardService.js";
import {objectToRows} from "@/utils/objectToRows.js";

const healthLabelMap = {
  status: 'Application',
  database: 'Database',
  docker: 'Docker',
  ollama: 'Ollama',
  model: 'Model',
  model_available: 'Model Available',
  reuse_threshold: 'Reuse Threshold',
  reference_threshold: 'Reference Threshold',
}
const translationMemoryLabelMap = {
  documentPairs: 'Document Pairs',
  translationUnits: 'Translation Units',
}

export const useDashboardStore = defineStore(
  'dashboard',
  () => {
    const health = ref(null)
    const configuration = ref(null)
    const translationMemory = ref(null)

    const loading = ref(false)
    const error = ref(null)

    async function getDashboard() {
      loading.value = true

      try {
        health.value = objectToRows(await await getHealth(), healthLabelMap,)
        translationMemory.value = objectToRows(await getTranslationMemoryStatistics(), translationMemoryLabelMap)
      } catch (err) {
        error.value = err
      } finally {
        loading.value = false
      }
    }

    return {
      health,
      configuration,
      translationMemory,

      loading,
      error,

      getDashboard,
    }
  },
)
