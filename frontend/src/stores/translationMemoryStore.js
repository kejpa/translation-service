import {ref, toRaw} from 'vue'
import {defineStore} from 'pinia'
import {
  deleteTranslationUnit,
  searchTranslationUnits,
  updateTranslationUnit
} from "@/services/translationMemoryService.js";

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
        } catch (err) {
          error.value =
            err.message ?? 'Search failed'
        } finally {
          loading.value = false
        }
      }

async function update() {
  loading.value = true

  error.value = null

  try {
    await updateTranslationUnit(
      selectedUnit.value,
    )

    await search()
  }

  catch (err) {
    error.value =
      err.message ??
      'Update failed'
  }

  finally {
    loading.value = false
  }
}

 async function remove() {
  if (!selectedUnit.value) {
    return
  }

  loading.value = true

  error.value = null

  try {
    await deleteTranslationUnit(
      selectedUnit.value.id,
    )

    selectedUnit.value = null

    await search()
  }
  catch (err) {
    error.value =
      err.message ??
      'Delete failed'
  }
  finally {
    loading.value = false
  }
}
      function selectUnit(unit) {
        selectedUnit.value = structuredClone(toRaw( unit))
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
