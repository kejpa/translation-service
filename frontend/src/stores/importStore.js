import {ref} from 'vue'
import {defineStore} from 'pinia'
import {importDocumentPair} from "@/services/importService.js";

export const useImportStore = defineStore('import', () => {
  const sourceFile = ref(null)
  const targetFile = ref(null)

  const loading = ref(false)
  const error = ref(null)

  const result = ref(null)

  function setSourceFile(file) {
    sourceFile.value = file
  }

  function setTargetFile(file) {
    targetFile.value = file
  }

  function clear() {
    sourceFile.value = null
    targetFile.value = null

    error.value = null
    result.value = null
  }

  async function importDocuments() {
    loading.value = true

    error.value = null
    result.value = null

    try {
      result.value = await importDocumentPair(sourceFile.value, targetFile.value,)
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  return {
    sourceFile, targetFile,

    loading, error,

    result,

    setSourceFile, setTargetFile,

    clear,

    importDocuments,
  }
},)
