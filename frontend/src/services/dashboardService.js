import {get} from './api'

export async function getServiceStatus() {
  return await get('/')
}

export async function getTranslationMemoryStatistics() {
  return await get('/translation-memory/statistics')
}

export async function getTranslationConfiguration() {
  return await get('/llm/config')
}
