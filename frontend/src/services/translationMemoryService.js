import {get, put, remove} from './api'

export async function searchTranslationUnits(
  query,
) {
  const encodedQuery = encodeURIComponent(
    query,
  )

  return await get(
    `/translation-units?query=${encodedQuery}`,
  )
}

export async function updateTranslationUnit(
  translationUnit,
) {
  return await put(
    `/translation-units/${translationUnit.id}`,
    {
      source_text:
      translationUnit.source_text,

      target_text:
      translationUnit.target_text,
    },
  )
}

export async function deleteTranslationUnit(
  id,
) {
  await remove(
    `/translation-units/${id}`,
  )
}
