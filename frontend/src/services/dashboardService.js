import {get} from './api'

export async function getHealth() {
  return await get('/health')
}

export async function getTranslationMemoryStatistics() {
  return {
    documentPairs: 12,
    translationUnits: 8421,
  }
}
