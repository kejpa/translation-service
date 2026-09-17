import {ref} from 'vue'
import {defineStore} from 'pinia'
import * as translateService from "@/services/translateService.js";

export const useTranslateStore = defineStore('translate', () => {
  const sourceFile = ref(null)
  const outputFilename = ref('translated.docx',)
  const loading = ref(false)
  const error = ref(null)
  const result = ref(null)

  function setSourceFile(file) {
    sourceFile.value = file
  }

  function clear() {
    sourceFile.value = null

    outputFilename.value = 'translated.docx'

    loading.value = false
    error.value = null

    result.value = null
  }

  async function translateDocument() {
    loading.value = true

    error.value = null
    result.value = null

    try {
      result.value = await translateService.translateDocument(sourceFile.value, outputFilename.value,)
    } catch (err) {
      error.value = err.message ?? 'Translation failed'
    } finally {
      loading.value = false
    }
  }

  return {
    sourceFile, outputFilename,

    loading, error,

    result,

    setSourceFile, clear, translateDocument,
  }
},)
