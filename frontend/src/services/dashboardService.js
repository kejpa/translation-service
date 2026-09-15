// src/services/dashboardService.js

export async function getHealth() {
  return {
    status: 'running',
    database: 'connected',
    docker: 'running',
    ollama: 'connected',
    model: 'gemma3:4b',
    model_available: true,
    reuse_threshold: 85,
    reference_threshold: 30,
  }
}

export async function getTranslationMemoryStatistics() {
  return {
    documentPairs: 12,
    translationUnits: 8421,
  }
}
