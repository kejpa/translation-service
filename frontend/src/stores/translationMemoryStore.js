import { ref } from 'vue'
import { defineStore } from 'pinia'
import {searchTranslationUnits} from "@/services/translationMemoryService.js";

export const useTranslationMemoryStore =
  defineStore(
    'translationMemory',
    () => {
      const query = ref('')

      const translationUnits = ref([])

      const loading = ref(false)
      const error = ref(null)

      const selectedUnit = ref(null)

      function clear() {
        query.value = ''

        translationUnits.value = []

        selectedUnit.value = null

        error.value = null
      }

  async function search() {
  loading.value = true

  error.value = null

  try {
    translationUnits.value =
      await searchTranslationUnits(
        query.value,
      )
  }
  catch (err) {
    error.value =
      err.message ?? 'Search failed'
  }
  finally {
    loading.value = false
  }
}
      async function update() {
        //
        // implementeras senare
        //
      }

      async function remove() {
        //
        // implementeras senare
        //
      }

      function selectUnit(unit) {
        selectedUnit.value = unit
      }

      return {
        query,

        translationUnits,

        loading,
        error,

        selectedUnit,

        clear,

        search,
        update,
        remove,

        selectUnit,
      }
    },
  )
