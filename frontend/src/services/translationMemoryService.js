import { get } from './api'

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
